import sqlite3
from werkzeug.security import generate_password_hash

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

    # SECURE: Store passwords as salted hashes
    users = [
        ('admin', generate_password_hash('admin')),
        ('user', generate_password_hash('password'))
    ]

    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

    # SECURE: We use a placeholder for supplier codes. 
    # In Phase 4, we will upgrade these to secure SHA-256 hashes.
    products = [
        ('Cyber-Shield Firewall', 299.99, 150, 'SUPPLIER-ALPHA-99'),
        ('Encrypted USB Drive', 44.99, 85, 'SUPPLIER-BETA-12'),
        ('Legacy Server Rack', 1199.99, 12, 'SUPPLIER-GAMMA-01'),
        ('Retro Mechanical Keyboard', 119.99, 210, 'SUPPLIER-DELTA-88'),
        ('Packet Sniffer Pro', 89.99, 64, 'SUPPLIER-EPSILON-44')
    ]
    cursor.executemany('INSERT INTO products (name, price, sales_count, supplier_code) VALUES (?, ?, ?, ?)', products)

    # Commit data and close connection
    connection.commit()
    connection.close()
    print("Database 'app.db' created and seeded successfully!")

if __name__ == "__main__":
    seed()
