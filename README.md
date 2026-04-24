# Vulnerable App: A Security Learning Laboratory

This project is a functional Flask web application designed to demonstrate common security vulnerabilities and their modern solutions. It transitions from a "Legacy/Vulnerable" state to a "Secure/Modern" state across two branches.

## 🚀 Project Overview

The application simulates a corporate product dashboard with a legacy authentication module written in C. It serves as a playground for identifying and patching critical security flaws.

### 🚩 Vulnerabilities (on `master` branch)
1.  **Buffer Overflow (CWE-120):** A legacy C library (`login_logic.dll`) uses `strcpy` on an undersized buffer, allowing authentication bypass via memory corruption.
2.  **SQL Injection (CWE-89):** The search bar uses unsafe string formatting, enabling data exfiltration via `UNION SELECT` attacks.
3.  **Weak Cryptography (CWE-327):** Sensitive supplier data is "protected" only by the obsolete MD5 algorithm.
4.  **Plaintext Passwords:** User credentials are stored in the database without hashing.
5.  **Broken Access Control:** Sensitive columns are hidden in the UI but still sent from the database to the application server.

### 🛡️ Secure Features (on `development` branch)
*   **Parameterized Queries:** Complete protection against SQL Injection.
*   **Secure Hashing:** Passwords stored using salted PBKDF2 hashes (Werkzeug).
*   **Memory Safety:** Retirement of the legacy C module in favor of native Python logic.
*   **Query-Level Access Control:** Sensitive data is never fetched from the DB for non-admin users.
*   **Strong Crypto:** Internal secrets protected with SHA-256.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
*   Python 3.10+
*   A C compiler (only needed if you wish to modify/rebuild the legacy C code on `master`)

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd vulnerable-app

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask werkzeug
```

### 3. Initialize the Database
```bash
python seed_db.py
```

### 4. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 🧪 Testing the Scenarios

### The Vulnerable Path (`git checkout master`)
1.  **Normal Login:** Log in with `user` / `password`.
2.  **The Leech (SQLi):** In the search bar, enter: `' UNION SELECT supplier_code, price, sales_count, '1' FROM products --` to see hidden supplier hashes.
3.  **The Bypass (Overflow):** Enter a very long password (e.g., `AAAAAAAAAAAA`) to bypass authentication using the legacy C library's buffer overflow.

### The Secure Path (`git checkout development`)
1.  **SQLi Test:** Try the same SQL injection. It will now return 0 results because it's treated as a literal search string.
2.  **Overflow Test:** The C library is gone; long passwords are simply rejected as invalid.
3.  **Access Control:** Log in as `user`. Even if you check the network traffic, the `supplier_code` is no longer being sent to the browser.

---

## 📂 Project Structure
*   `app.py`: The main Flask web server.
*   `seed_db.py`: Database initialization script.
*   `templates/`: HTML layouts (Jinja2).
*   `static/`: CSS styling.
*   `legacy-codebase/`: (Master only) The vulnerable C source and DLL.

**Educational Purpose:** This app is for learning only. Never use these patterns in production environments.
