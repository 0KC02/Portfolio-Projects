import sqlite3
import os
from cryptography.fernet import Fernet
import hashlib
import base64

class Database:
    def __init__(self, db_path="password_manager.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create master password table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_password (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')
        
        # Create passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password_encrypted TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def set_master_password(self, password_hash):
        """Set or update the master password hash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM master_password')
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute('INSERT INTO master_password (password_hash) VALUES (?)', (password_hash,))
        else:
            cursor.execute('UPDATE master_password SET password_hash = ? WHERE id = 1', (password_hash,))
        
        conn.commit()
        conn.close()
    
    def get_master_password_hash(self):
        """Retrieve the master password hash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT password_hash FROM master_password LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def has_master_password(self):
        """Check if master password exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM master_password')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_encryption_key(self, master_password):
        """Generate encryption key from master password"""
        # Use SHA-256 to derive a key, then encode to base64 for Fernet
        key = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(key)
    
    def encrypt_password(self, password, master_password):
        """Encrypt a password using the master password"""
        key = self.get_encryption_key(master_password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(password.encode())
        return encrypted.decode()
    
    def decrypt_password(self, encrypted_password, master_password):
        """Decrypt a password using the master password"""
        try:
            key = self.get_encryption_key(master_password)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception:
            return None
    
    def add_password(self, website, username, password, master_password):
        """Add a new password entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        encrypted_password = self.encrypt_password(password, master_password)
        
        cursor.execute('''
            INSERT INTO passwords (website, username, password_encrypted)
            VALUES (?, ?, ?)
        ''', (website, username, encrypted_password))
        
        conn.commit()
        conn.close()
    
    def get_all_passwords(self, master_password):
        """Retrieve all password entries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, website, username, password_encrypted FROM passwords')
        rows = cursor.fetchall()
        conn.close()
        
        passwords = []
        for row in rows:
            decrypted = self.decrypt_password(row[3], master_password)
            if decrypted:
                passwords.append({
                    'id': row[0],
                    'website': row[1],
                    'username': row[2],
                    'password': decrypted
                })
        
        return passwords
    
    def search_passwords(self, query, master_password):
        """Search passwords by website or username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, website, username, password_encrypted 
            FROM passwords 
            WHERE website LIKE ? OR username LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        passwords = []
        for row in rows:
            decrypted = self.decrypt_password(row[3], master_password)
            if decrypted:
                passwords.append({
                    'id': row[0],
                    'website': row[1],
                    'username': row[2],
                    'password': decrypted
                })
        
        return passwords
    
    def update_password(self, password_id, website, username, password, master_password):
        """Update an existing password entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        encrypted_password = self.encrypt_password(password, master_password)
        
        cursor.execute('''
            UPDATE passwords 
            SET website = ?, username = ?, password_encrypted = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (website, username, encrypted_password, password_id))
        
        conn.commit()
        conn.close()
    
    def delete_password(self, password_id):
        """Delete a password entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
        
        conn.commit()
        conn.close()

