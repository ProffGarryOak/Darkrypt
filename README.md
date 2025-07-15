![image](https://github.com/user-attachments/assets/d651694a-e12b-4e91-8886-a4e380dbfbed)

DarKrypt Diary is a personal encrypted diary application that allows users to securely store private messages, thoughts, and notes. Each entry is encrypted using the Vigenère cipher, ensuring that your data remains safe and protected.

## Features

- **Secure Entries**: Create, edit, and view encrypted diary entries.
- **Unique Encryption**: Each note is encrypted with a unique cipher key.
- **Decryption**: Decrypt your notes whenever needed, keeping your secrets safe.
- **User Authentication**: Login and manage your encrypted notes.

## Screenshots

![image](https://github.com/user-attachments/assets/daf9546e-35d2-4636-b567-ab9287097e26)
![image](https://github.com/user-attachments/assets/c6afe6a6-d8dc-410c-85b8-055fc4e67f6b)
![image](https://github.com/user-attachments/assets/5aa1a587-6b2a-4c00-8345-ebdec07d0a22)
![image](https://github.com/user-attachments/assets/933e6416-fd77-499d-8890-936b4ef7640f)
![image](https://github.com/user-attachments/assets/cb912a78-197c-4824-8e27-a85fd236a623)


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ProffGarryOak/Darkrypt.git
   cd Darkrypt
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## Technologies Used

- **Flask**: Backend framework
- **HTML, CSS, JavaScript**: Frontend development
- **Vigenère Cipher**: Encryption algorithm
- **Bootstrap**: UI styling

## Future Improvements

- **Enhanced Encryption**: Implement more robust encryption algorithms.
- **Rich Text Editor**: Allow formatting within diary entries.
- **Search Functionality**: Enable searching within encrypted notes.
- **Mobile Optimization**: Improve user experience on mobile devices.

## Contributing

Contributions are welcome. Feel free to submit pull requests or report issues in the repository.
