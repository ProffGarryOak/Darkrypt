from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mongo_client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
db = mongo_client['vigenere_db']
users_collection = db['users']
notes_collection = db['notes']

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

def make_table(key):
    key = key.upper()
    alphabet = [chr(i) for i in range(65, 91)]
    alphabet += " "
    remaining = [ch for ch in alphabet if ch not in key]
    line1 = list(key) + remaining
    result = []
    for i in range(27):
        nextline = line1[i:] + line1[:i]
        result.append(nextline)
    return result

def encrypt(coded_table, message, key):
    message = message.upper()
    message = ''.join(char for char in message if (char.isalpha() or char == " "))
    key = key.upper()
    repeated_key = (key * (len(message) // len(key) + 1))[:len(message)]
    encrypted_text = []
    for msg_char, key_char in zip(message, repeated_key):
        row_index = coded_table[0].index(msg_char)
        col_index = coded_table[0].index(key_char)
        encrypted_char = coded_table[row_index][col_index]
        encrypted_text.append(encrypted_char)
    return ''.join(encrypted_text)

def decipher(coded_table, cipher_text, key):
    cipher_text = cipher_text.upper()
    key = key.upper()
    repeated_key = (key * (len(cipher_text) // len(key) + 1))[:len(cipher_text)]
    decipher_text = []
    for cipher_char, key_char in zip(cipher_text, repeated_key):
        row_index = coded_table[0].index(key_char)
        for i in range(27):
            if coded_table[row_index][i] == cipher_char:
                col_index = i
                break
        decipher_char = coded_table[0][col_index]
        decipher_text.append(decipher_char)
    return ''.join(decipher_text)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(str(user['_id']))
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Failed. Check your username and password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    result = None
    if request.method == 'POST':
        table_key = request.form['table_key']
        coded_table = make_table(table_key)
        cipher_key = request.form['cipher_key']
        message = request.form['message']
        heading = request.form['heading']
        result = encrypt(coded_table, message, cipher_key)
        noted_id = notes_collection.insert_one({
            "user_id": current_user.id,
            "heading": heading,
            "message": result
        }).inserted_id  # Store the note's ID
        flash('Note saved successfully!', 'success')  # Flash message for note save
    notes = list(notes_collection.find({"user_id": current_user.id}, {"_id": 1, "heading": 1}))
    return render_template('index.html', result=result, notes=notes)

@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
@login_required
def view_note(note_id):
    # Convert note_id from string to ObjectId if needed
    try:
        note_id = ObjectId(note_id)
    except Exception as e:
        print("Error in finding note id", note_id)
        return "Invalid note id"

    # Find the document in the notes collection by its _id
    note = notes_collection.find_one({"_id": note_id})
    if not note:
        print('Note not found', note_id)
        return "Note not found"

    decrypted_message = None
    if request.method == 'POST':
        table_key = request.form['table_key']
        cipher_key = request.form['cipher_key']
        coded_table = make_table(table_key)
        message = note['message']
        decrypted_message = decipher(coded_table, message, cipher_key)

    return render_template('view_note.html', note=note, decrypted_message=decrypted_message)

    

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
