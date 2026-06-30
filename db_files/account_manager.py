import tkinter as tk                # GUI library for application interface
import re                           # Regular expressions for input validation
import os                           # File handling
import json                         # Data storage
import time                         # Rate-limiting for login
import hashlib                      # Secure password hashing
from datetime import datetime       # Date input validation
from system_functions.backend.ui_helpers import bind_exit_home # Helper function to bind Escape key to exit menus
from db_files.data_manager import load_data, create_backup # Import safe loading and backup creation

# DATABASE SETUP
ACCOUNTDB_FILE = "db_files/users.json"
ACCOUNTDB_BACKUP = "db_files/backup/users_backup.json"

MAX_LOGIN_ATTEMPTS = 5   # Maximum login attempts before lockout
LOCKOUT_TIME = 60        # Lockout time (60 seconds)

failed_attempts = {} # Dictionary to store failed login attempts for each user

# ENSURE DATABASE FILE EXISTS
if not os.path.exists(ACCOUNTDB_FILE):
    with open(ACCOUNTDB_FILE, "w") as f:
        json.dump({}, f)
    
    create_backup(ACCOUNTDB_FILE, ACCOUNTDB_BACKUP) # Create a backup of the user account file

# SECURITY FEATURE (PASSWORD HASHING)
def hash_password(password):
    """Simple hashing with SHA-256 (will switch to bcrypt in the future)"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email): 
    """
    Simple regex for email validation during signup

    Requirements: 
    - Must contain '@' symbol
    - Must contain '.' symbol
    - Must not contain any whitespace characters
    """
    return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)

def validate_password(password): 
    """
    Simple regex for password validation during signup

    Requirements:
    - Minimum 8 characters
    - Must contain at least one letter
    - Must contain at least one number"""
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password)

def validate_dob(dob):
    """Check if DOB is in correct format and not in the future"""
    try:
        return datetime.strptime(dob, "%Y-%m-%d") <= datetime.now()
    except:
        return False

def save_user(username, email, dob, password):
    """
    Save a user account to the database.
    Returns True if the user was saved successfully, False if the username already exists (case-insensitive).
    """
    data = load_data(ACCOUNTDB_FILE)

    # Check case-insensitive duplicates
    for existing_user in data:
        if existing_user.lower() == username.lower():
            return False

    # Store user data in a dictionary
    data[username] = {
        "username": username,
        "email": email,
        "dob": dob,
        "password": hash_password(password),
        "streak": 0,
        "best_streak": 0,
        "last_login_date": ""
    }

    with open(ACCOUNTDB_FILE, "w") as f: # Save updated user data back to JSON file
        json.dump(data, f, indent=4)

    create_backup(ACCOUNTDB_FILE, ACCOUNTDB_BACKUP)
    return True # Return True if user was saved successfully, False if username already exists (case-insensitive)

def update_login_streak(username):
    """Update login streak for a user"""
    data = load_data(ACCOUNTDB_FILE) # Load user account data from JSON file

    if username not in data:
        return

    user = data[username] # Get user account data
    today = datetime.now().date() # Get current date
    last_login = user.get("last_login_date", "") # Get last login date from user account data

    # First login ever
    if last_login == "":
        user["streak"] = 1
        user["best_streak"] = 1
        user["last_login_date"] = today.strftime("%Y-%m-%d")

    else:
        last_login_date = datetime.strptime(last_login, "%Y-%m-%d").date()
        difference = (today - last_login_date).days

        # Same day
        if difference == 0:
            pass

        # Consecutive day
        elif difference == 1:
            user["streak"] += 1

            if user["streak"] > user.get("best_streak", 0):
                user["best_streak"] = user["streak"]

            user["last_login_date"] = today.strftime("%Y-%m-%d")

        # Missed one or more days
        else:
            # Reset streak but keep best streak record
            user["streak"] = 1
            user["last_login_date"] = today.strftime("%Y-%m-%d")

    with open(ACCOUNTDB_FILE, "w") as f:
        json.dump(data, f, indent=4)

    create_backup(ACCOUNTDB_FILE, ACCOUNTDB_BACKUP) # Create a backup of the user account file

def user_registration(self):
    """User registration screen"""
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

    def dupe_username_error(username):
        data = load_data(ACCOUNTDB_FILE)

        for existing_user in data:
            if existing_user.lower() == username.lower():
                return True

        return False

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
        elif dupe_username_error(username.get()):
            error_username.config(text="User already exists")
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
            error_password.config(text="Weak password (at least 8 characters long + at least 1 number)")
            valid = False
        else:
            error_password.config(text="")

        submit_btn.config(state="normal" if valid else "disabled")

    for field in [username, email, dob, password]: # Bind validation to all fields on key release
        field.bind("<KeyRelease>", lambda e: validate())

    def submit(): 
        save_user(username.get(), email.get(), dob.get(), password.get())

        # Submit function to save user data after validation
        self.current_user = username.get()
        update_login_streak(self.current_user)
        self.show_main_menu()
        self.play_music()

    # Buttons (submit button starts disabled and only enables when all fields are valid)
    submit_btn = tk.Button(frame, text="Register", state="disabled", command=submit, bg=self.ACCENT, fg=self.TEXT, width=20, height=2)
    submit_btn.pack(pady=10)
    tk.Button(frame, text="← Back", command=self.show_home, bg=self.BG_CARD, fg=self.TEXT, width=20, height=2).pack(pady=10)

    bind_exit_home(self) # Bind Escape key to exit back to home screen

def user_login(self):
    """User login screen"""
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
        data = load_data(ACCOUNTDB_FILE)

        input_username = username.get().strip().lower() # Normalize username to lowercase
        user = None # Initialize user data placeholder

        # Check whether this username is currently locked out
        if input_username in failed_attempts:
            attempts, lock_time = failed_attempts[input_username]

            if attempts >= MAX_LOGIN_ATTEMPTS:
                # User is locked out
                elapsed = time.time() - lock_time # Calculate elapsed time since lockout

                if elapsed < LOCKOUT_TIME:
                    remaining = int(LOCKOUT_TIME - elapsed) # Calculate remaining time for lockout in seconds
                    general_error.config(text=f"Too many failed attempts. Try again in {remaining}s.")
                    return
                else:
                    # Lockout expired
                    failed_attempts.pop(input_username) # Remove the user from the failed attempts dictionary

        for existing_user in data:
            # Case-insensitive username check to find the correct user data
            if existing_user.lower() == input_username.lower():
                user = data[existing_user]
                break

        if not user or user["password"] != hash_password(password.get()):
            # Invalid username or password
            if input_username not in failed_attempts:
                failed_attempts[input_username] = [1, 0] # Initialize failed attempts count and lockout time
            else:
                failed_attempts[input_username][0] += 1 # Increment failed attempts count

                if failed_attempts[input_username][0] >= MAX_LOGIN_ATTEMPTS: # User is locked out
                    failed_attempts[input_username][1] = time.time() # Record the lockout time

            remaining = max(0, MAX_LOGIN_ATTEMPTS - failed_attempts[input_username][0]) # Calculate remaining attempts

            if remaining > 0:
                general_error.config(text=f"Invalid username or password ({remaining} attempts left)")
            else:
                general_error.config(text=f"Too many failed attempts. Locked for {LOCKOUT_TIME} seconds.")

            return

        self.current_user = user["username"] # Set current user to the logged-in user
        failed_attempts.pop(input_username, None) # Remove the user from the failed attempts dictionary
        update_login_streak(self.current_user) # Update login streak after successful login
        self.show_main_menu()
        self.play_music()

    # Buttons (login starts disabled until user types something, back button to return to home screen)
    login_btn = tk.Button(frame, text="Log In", state="disabled", command=login, bg=self.ACCENT, fg=self.TEXT, width=20, height=2)
    login_btn.pack(pady=10)
    tk.Button(frame, text="← Back", command=self.show_home, bg=self.BG_CARD, fg=self.TEXT, width=20, height=2).pack(pady=10)

    bind_exit_home(self)