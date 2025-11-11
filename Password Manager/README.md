# Password Manager

A secure password manager built with Python, tkinter, and SQLite.

## Features

- **Secure Storage**: Passwords are encrypted using Fernet symmetric encryption before being stored in the database
- **Master Password**: First-time setup creates a master password that protects all stored passwords
- **Password Management**: Add, edit, delete, and search passwords
- **Password Generator**: Generate strong random passwords with customizable options
- **Password Strength Analyzer**: Real-time password strength feedback
- **User-Friendly GUI**: Clean and intuitive interface built with tkinter

## Installation

1. Install Python 3.7 or higher

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the password manager:
```bash
python password_manager.py
```

### First Time Setup

1. When you first run the application, you'll be prompted to set a master password
2. Enter a master password (minimum 8 characters)
3. Confirm the master password
4. Once set, you can start adding passwords

### Managing Passwords

- **Add Password**: Go to the "Add/Edit Password" tab, fill in website, username, and password, then click "Save Password"
- **View Passwords**: All passwords are listed in the "View Passwords" tab
- **Search**: Use the search box to filter passwords by website or username
- **Edit**: Select a password and click "Edit" or double-click to load it into the edit form
- **Delete**: Select a password and click "Delete"
- **View Details**: Select a password and click "View" to see the full password with copy functionality

### Password Generator

- Set password length (8-64 characters)
- Choose character types: uppercase, lowercase, numbers, symbols
- Click "Generate" to create a random password
- The generated password will appear in the password field

### Password Strength Analysis

As you type a password, the strength indicator shows:
- **Very Weak** (0-2/9)
- **Weak** (3-4/9)
- **Fair** (5-6/9)
- **Good** (7/9)
- **Strong** (8-9/9)

## Security Features

- Master password is hashed using SHA-256
- Individual passwords are encrypted using Fernet (symmetric encryption)
- Encryption key is derived from the master password
- Passwords are decrypted only when needed and displayed

## Database

The application uses SQLite to store encrypted passwords. The database file (`password_manager.db`) is created automatically in the same directory as the application.

## Notes

- Remember your master password! It cannot be recovered if forgotten
- Keep your master password secure and unique
- The database file contains encrypted data, but you should still keep it secure

