import sqlite3
import hashlib

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

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

    # Insert Mock Users (Plaintext passwords for legacy system)
    users = [
        ('admin', 'admin'),
        ('user', 'password')
    ]

    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

    # Insert Top Selling Products (with MD5 hashed supplier codes)
    products = [
        ('Cyber-Shield Firewall', 299.99, 150, md5_hash('ONE')),
        ('Encrypted USB Drive', 44.99, 85, md5_hash('TWO')),
        ('Legacy Server Rack', 1199.99, 12, md5_hash('ONE')),
        ('Retro Mechanical Keyboard', 119.99, 210, md5_hash('THREE')),
        ('Packet Sniffer Pro', 89.99, 64, md5_hash('FOUR'))
    ]
    cursor.executemany('INSERT INTO products (name, price, sales_count, supplier_code) VALUES (?, ?, ?, ?)', products)

    # Commit data and close connection
    connection.commit()
    connection.close()
    print("Database 'app.db' created and seeded successfully!")

if __name__ == "__main__":
    seed()