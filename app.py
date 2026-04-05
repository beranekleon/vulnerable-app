import ctypes
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# Load the legacy library
login_lib = ctypes.CDLL('./legacy-codebase/login_logic.dll')

# Configure the legacy library's input and output types
# 'argtypes' defines what we send to C (a char pointer)
# 'restype' defines what we get back (an integer)
login_lib.verify_login.argtypes = [ctypes.c_char_p]
login_lib.verify_login.restype = ctypes.c_int

# Flask needs a secret key to encrypt session cookies
# In development, any string works, but in prodcution, you need a random, complex key
app.secret_key = 'super_secret_key'

def get_db_connection():
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row # Allows accessing columns by name
    return connection

# Route to landing page
@app.route("/")
def home():
    return render_template("landing.html")

# Route to login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        
        # Convert Python string to bytes for C compatibility
        password_bytes = password.encode('utf-8')
        
        # Call the C function
        result = login_lib.verify_login(password_bytes)
        
        if result != 0:
            # Handle successful login
            # Store the login state in the session cookie
            session['logged_in'] = True
            session['username'] = request.form.get("username")

            # Redirect the user to the dashboard route
            return redirect(url_for('dashboard'))
        else:
            session.clear()
            return "<h1>Access Denied</h1><p>Password incorrect.</p>"
    return render_template("login.html")

# Route to dashboard page
@app.route("/dashboard")
def dashboard():
    # If the 'logged_in' key isn't in the session cookies, the user is not authenticated
    # --> redirect them back to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # If authenticated, show the dashboard page
    connection = get_db_connection()
    products = connection.execute('SELECT * FROM products ORDER BY sales_count DESC LIMIT 3').fetchall()
    connection.close()
    return render_template("dashboard.html", username = session.get('username'),products=products   )

# Logout Route
@app.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()