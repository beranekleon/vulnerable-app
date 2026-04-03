import ctypes
from flask import Flask, render_template, request

app = Flask(__name__)

# 1. Load the shared library
login_lib = ctypes.CDLL('./legacy-codebase/login_logic.dll')

# 2. Configure the function's input and output types
# 'argtypes' defines what we send to C (a char pointer)
# 'restype' defines what we get back (an integer)
login_lib.verify_login.argtypes = [ctypes.c_char_p]
login_lib.verify_login.restype = ctypes.c_int

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        
        # 3. Convert Python string to bytes for C compatibility
        password_bytes = password.encode('utf-8')
        
        # 4. Call the C function
        result = login_lib.verify_login(password_bytes)
        
        if result != 0:
            return "<h1>Login Successful!</h1><p>The buffer overflow worked (or you knew the password).</p>"
        else:
            return "<h1>Access Denied</h1><p>Try a longer 'password' to trigger the overflow.</p>"
            
    return render_template("login.html")

if __name__ == "__main__":
    app.run()