import tkinter as tk                # GUI library for application interface
import re                           # Regular expressions for input validation
import json                         # Data storage
import os                           # File handling
import hashlib                      # Secure password hashing
from datetime import datetime       # Date input validation
from system_functions.backend.ui_helpers import bind_exit_home # Helper function to bind Escape key to exit menus

# DATABASE SETUP
ACCOUNTDB_FILE = "db_files/users.json"

# ENSURE DATABASE FILE EXISTS
if not os.path.exists(ACCOUNTDB_FILE):
    with open(ACCOUNTDB_FILE, "w") as f:
        json.dump({}, f)

# SECURITY FEATURE (PASSWORD HASHING)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() # Simple hashing for demonstration (use bcrypt/scrypt in production)

# USER ACCOUNT VALIDATION
def validate_email(email): 
    # Simple regex for email validation
    return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)

def validate_password(password): 
    # Minimum 8 characters, at least one letter and one number
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password)

def validate_dob(dob):
    # Check if DOB is in correct format and not in the future
    try:
        return datetime.strptime(dob, "%Y-%m-%d") <= datetime.now()
    except:
        return False

# SAVE USER TO ACCOUNTS DATABASE
def save_user(username, email, dob, password):
    with open(ACCOUNTDB_FILE, "r") as f:
        data = json.load(f)

    # Check case-insensitive duplicates
    for existing_user in data:
        if existing_user.lower() == username.lower():
            return False

    data[username] = { # Storing user data (password is hashed for security)
        "username": username, # Username
        "email": email, # Email
        "dob": dob, # Date of Birth
        "password": hash_password(password), # Hashed password
        "streak": 0 # Streak (currently placeholder)
    }

    with open(ACCOUNTDB_FILE, "w") as f: # Save updated user data back to JSON file
        json.dump(data, f, indent=4)

    return True # Return True if user was saved successfully, False if username already exists (case-insensitive)

# REGISTRATION SCREEN
def user_registration(self):
    self.clear()

    # Registration frame, dark background
    outer = tk.Frame(self.root, bg=self.BG_MAIN)
    outer.pack(expand=True)

    frame = tk.Frame(outer, bg=self.BG_CARD, padx=100, pady=40)
    frame.pack()

    tk.Label(frame, text="Register", font=("Segoe UI", 26, "bold"), bg=self.BG_CARD, fg=self.TEXT).pack(pady=10)

    username, error_username = self.create_field(frame, "Username") # Username field with error label
    email, error_email = self.create_field(frame, "Email") # Email field with error label
    dob, error_dob = self.create_field(frame, "Date of Birth (YYYY-MM-DD)") # DOB field with error label
    password, error_password = self.create_field(frame, "Password", is_password=True) # Password field with error label

    general_error = tk.Label(frame, text="", fg="red", bg=self.BG_CARD)
    general_error.pack() # General error (e.g. user already exists)

    # VALIDATION MECHANISM
    def validate():
        valid = True # Assume valid until checks fail

        # USERNAME
        if username.get().strip() == "": # Check if username is empty
            error_username.config(text="Username required")
            valid = False
        elif len(username.get()) < 3: # Check if username is too short
            error_username.config(text="Username too short")
            valid = False
        elif len(username.get()) > 20: # Check if username is too long
            error_username.config(text="Username too long")
            valid = False
        elif not re.match(r"^[a-zA-Z0-9_]+$", username.get()): # Check if username contains invalid characters
            error_username.config(text="Only letters, numbers, _")
            valid = False
        else:
            error_username.config(text="")

        # EMAIL
        if not validate_email(email.get()): # Check if email is valid
            error_email.config(text="Invalid email")
            valid = False
        else:
            error_email.config(text="")

        # DOB
        if not validate_dob(dob.get()): # Check if DOB is valid
            error_dob.config(text="Invalid DOB")
            valid = False
        else:
            error_dob.config(text="")

        # PASSWORD
        if not validate_password(password.get()): # Check if password is strong enough
            error_password.config(text="Weak password")
            valid = False
        else:
            error_password.config(text="")

        submit_btn.config(state="normal" if valid else "disabled")

    for field in [username, email, dob, password]: # Bind validation to all fields on key release
        field.bind("<KeyRelease>", lambda e: validate())

    def submit(): 
        # Submit function to save user data after validation
        if not save_user(username.get(), email.get(), dob.get(), password.get()):
            general_error.config(text="User already exists") # Check if user already exists and show error
            return

        self.current_user = username.get()
        self.show_main_menu()

    # Buttons (submit button starts disabled and only enables when all fields are valid)
    submit_btn = tk.Button(frame, text="Submit", state="disabled", command=submit, bg=self.ACCENT, fg=self.TEXT, width=20, height=2)
    submit_btn.pack(pady=10)
    tk.Button(frame, text="← Back", command=self.show_home, bg=self.BG_CARD, fg=self.TEXT, width=20, height=2).pack(pady=10)

    bind_exit_home(self) # Bind Escape key to exit back to home screen

def user_login(self):
    # LOGIN SCREEN (BASIC)
    self.clear()

    # Same outer structure as registration for consistency
    outer = tk.Frame(self.root, bg=self.BG_MAIN)
    outer.pack(expand=True)

    frame = tk.Frame(outer, bg=self.BG_CARD, padx=100, pady=40)
    frame.pack()

    tk.Label(frame, text="Login", font=("Segoe UI", 26, "bold"), bg=self.BG_CARD, fg=self.TEXT).pack(pady=10)

    # Input fields
    username, _ = self.create_field(frame, "Username")
    password, _ = self.create_field(frame, "Password", is_password=True)

    general_error = tk.Label(frame, text="", fg="red", bg=self.BG_CARD)
    general_error.pack()

    # Enable button when user types something in either field, redisable if empty
    def enable_button(event=None):
        if username.get().strip() != "" or password.get().strip() != "":
            login_btn.config(state="normal")
        else:
            login_btn.config(state="disabled")

    username.bind("<KeyRelease>", enable_button)
    password.bind("<KeyRelease>", enable_button)

    def login():
        # Main login logic handler
        with open(ACCOUNTDB_FILE, "r") as f:
            data = json.load(f)

        input_username = username.get()
        user = None

        for existing_user in data:
            # Case-insensitive username check to find the correct user data
            if existing_user.lower() == input_username.lower():
                user = data[existing_user]
                break

        if not user or user["password"] != hash_password(password.get()):
            # If user not found or password doesn't match, show general error (doesn't specify which one for security)
            general_error.config(text="Invalid username or password")
            return

        self.current_user = user["username"]
        self.show_main_menu()

    # Buttons (login starts disabled until user types something, back button to return to home screen)
    login_btn = tk.Button(frame, text="Log In", state="disabled", command=login, bg=self.ACCENT, fg=self.TEXT, width=20, height=2)
    login_btn.pack(pady=10)
    tk.Button(frame, text="← Back", command=self.show_home, bg=self.BG_CARD, fg=self.TEXT, width=20, height=2).pack(pady=10)

    bind_exit_home(self)