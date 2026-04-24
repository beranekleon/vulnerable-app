from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

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
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Fetch the stored password hash from the database
        connection = get_db_connection()
        user = connection.execute('SELECT password FROM users WHERE username = ?', (username,)).fetchone()
        connection.close()

        # SECURE AUTH: Compare the input with the stored salted hash in memory-safe Python.
        # This replaces the legacy C library entirely.
        if user and check_password_hash(user['password'], password):
            # Handle successful login
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        session.clear()
        return render_template("login.html", error="Access Denied: Invalid username or password.")
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

@app.route("/search")
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    query_param = request.args.get('q', '')
    
    conn = get_db_connection()
    
    # SECURE CODE: Using a parameterized query (?) ensures that the 
    # database treats the input strictly as a string, not as a command.
    safe_query = "SELECT name, price, sales_count, supplier_code FROM products WHERE name LIKE ?"
    search_pattern = f"%{query_param}%"
    
    print(f"Executing Secure Query for pattern: {search_pattern}")
    
    try:
        results = conn.execute(safe_query, (search_pattern,)).fetchall()
    except Exception as e:
        # If the attacker writes bad SQL, show the error (classic 'Error-Based SQLi')
        return f"Database Error: {str(e)}"
    finally:
        conn.close()

    return render_template("dashboard.html", 
                           username=session.get('username'), 
                           products=results, 
                           search_term=query_param)

# Logout Route
@app.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
