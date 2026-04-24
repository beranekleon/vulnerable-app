import sqlite3
import hashlib
from werkzeug.security import generate_password_hash

def secure_hash(text):
    # Using SHA-256: A modern, high-integrity cryptographic hash.
    return hashlib.sha256(text.encode()).hexdigest()

def seed():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    # Create Tables
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            sales_count INTEGER DEFAULT 0,
            supplier_code TEXT
        )
    ''')

    # SECURE: Store passwords as salted PBKDF2 hashes
    users = [
        ('admin', generate_password_hash('admin')),
        ('user', generate_password_hash('password'))
    ]

    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

    # SECURE: Sensitive supplier data is now protected with SHA-256 hashes
    products = [
        ('Cyber-Shield Firewall', 299.99, 150, secure_hash('SUPPLIER-ALPHA-99')),
        ('Encrypted USB Drive', 44.99, 85, secure_hash('SUPPLIER-BETA-12')),
        ('Legacy Server Rack', 1199.99, 12, secure_hash('SUPPLIER-GAMMA-01')),
        ('Retro Mechanical Keyboard', 119.99, 210, secure_hash('SUPPLIER-DELTA-88')),
        ('Packet Sniffer Pro', 89.99, 64, secure_hash('SUPPLIER-EPSILON-44'))
    ]
    cursor.executemany('INSERT INTO products (name, price, sales_count, supplier_code) VALUES (?, ?, ?, ?)', products)

    # Commit data and close connection
    connection.commit()
    connection.close()
    print("Database 'app.db' created and seeded successfully with SHA-256 hashes!")

if __name__ == "__main__":
    seed()
