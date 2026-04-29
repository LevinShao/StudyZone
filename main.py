import tkinter as tk
from tkinter import messagebox
import re
import json
import os
import hashlib
from datetime import datetime
from PIL import Image, ImageTk

# DATABASE SETUP
DB_FILE = "users.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
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
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)

def validate_dob(dob):
    # Check if DOB is in correct format and not in the future
    try:
        return datetime.strptime(dob, "%Y-%m-%d") <= datetime.now()
    except:
        return False

# SAVE USER TO ACCOUNTS DATABASE
def save_user(username, email, dob, password):
    with open(DB_FILE, "r") as f:
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

    with open(DB_FILE, "w") as f: # Save updated user data back to JSON file
        json.dump(data, f, indent=4)

    return True # Return True if user was saved successfully, False if username already exists (case-insensitive)

# APP CLASS
class StudyZoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyZone")

        # Fullscreen but keeps taskbar & buttons
        self.root.state("zoomed")
        self.root.configure(bg="#111111")

        self.show_home()

    # CLEAR SCREEN
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # HOME SCREEN
    def show_home(self):
        self.clear()

        # Main container for home screen
        container = tk.Frame(self.root, bg="#111111")
        container.pack(expand=True)

        # LOGO AREA
        logo_frame = tk.Frame(container, bg="#111111")
        logo_frame.pack(pady=40)

        logo_path = os.path.join(os.path.dirname(__file__), "img_assets/StudyZone.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((900, 300)) # Resize logo to fit better on screen
            self.icon = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self.icon, bg="#111111").pack(side="left")
        else:
            print(f"Logo image not found --> {logo_path}") # Print error when logo is not found

        # BUTTON AREA (LOWER POSITION)
        button_frame = tk.Frame(container, bg="#111111")
        button_frame.pack(pady=100)

        # Front menu buttons
        tk.Button(button_frame, text="Register", command=self.show_register, bg="red", fg="white", width=20, height=2).pack(pady=10) # Register
        tk.Button(button_frame, text="Log In", command=self.show_login, bg="#333", fg="white", width=20, height=2).pack(pady=10) # Log In

    # REGISTER SCREEN
    def show_register(self):
        self.clear()

        # Registration frame, dark background
        frame = tk.Frame(self.root, bg="#1a1a1a", padx=30, pady=30)
        frame.pack(expand=True)

        tk.Label(frame, text="Register", font=("Poppins", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)

        def create_field(label): 
            # Helper function to create labeled entry fields with error labels
            tk.Label(frame, text=label, bg="#1a1a1a", fg="white").pack(anchor="w")

            entry = tk.Entry(frame, bg="#222", fg="white", insertbackground="white", width=50)
            entry.pack(fill="x", pady=10) # Entry field for user input
            error = tk.Label(frame, text="", fg="red", bg="#1a1a1a", font=("Arial", 8))
            error.pack(anchor="w") # Error label for validation messages (initially empty)

            return entry, error # Return both the entry widget and its associated error label for validation

        username, err_username = create_field("Username") # Username field with error label
        email, err_email = create_field("Email") # Email field with error label
        dob, err_dob = create_field("DOB (YYYY-MM-DD)") # DOB field with error label

        # Password field
        tk.Label(frame, text="Password", bg="#1a1a1a", fg="white").pack(anchor="w", pady=(10,0))

        # Password frame +  toggle visibility
        pass_frame = tk.Frame(frame, bg="#1a1a1a")
        pass_frame.pack(fill="x")
        password = tk.Entry(pass_frame, show="*", bg="#222", fg="white", insertbackground="white", width=50)
        password.pack(side="left", fill="x", expand=True)

        def toggle(): 
            # Toggle password visibility function
            password.config(show="" if password.cget("show") == "*" else "*")

        tk.Button(pass_frame, text="👁", command=toggle, bg="#333", fg="white").pack(side="right") # Toggle button

        # Error labels
        err_pass = tk.Label(frame, text="", fg="red", bg="#1a1a1a", font=("Arial", 8))
        err_pass.pack(anchor="w") # Password error
        general_error = tk.Label(frame, text="", fg="red", bg="#1a1a1a")
        general_error.pack() # General error (e.g. user already exists)

        # VALIDATION MECHANISM
        def validate():
            valid = True # Assume valid until checks fail

            if username.get().strip() == "": # Check if username is empty
                err_username.config(text="Username required")
                valid = False
            else:
                err_username.config(text="")

            if not validate_email(email.get()): # Check if email is valid
                err_email.config(text="Invalid email")
                valid = False
            else:
                err_email.config(text="")

            if not validate_dob(dob.get()): # Check if DOB is valid
                err_dob.config(text="Invalid DOB")
                valid = False
            else:
                err_dob.config(text="")

            if not validate_password(password.get()): # Check if password is strong enough
                err_pass.config(text="Weak password")
                valid = False
            else:
                err_pass.config(text="")

            submit_btn.config(state="normal" if valid else "disabled")

        for field in [username, email, dob, password]: # Bind validation to all fields on key release
            field.bind("<KeyRelease>", lambda e: validate())

        def submit(): 
            # Submit function to save user data after validation
            if not save_user(username.get(), email.get(), dob.get(), password.get()):
                general_error.config(text="User already exists") # Check if user already exists and show error
                return

            messagebox.showinfo("Success", "Registered!")
            self.show_home() # Placeholder for future updates

        # Submit button starts disabled and only enables when all fields are valid
        submit_btn = tk.Button(frame, text="Submit", state="disabled", command=submit, bg="red", fg="white")
        submit_btn.pack(pady=10)

        tk.Button(frame, text="← Back", command=self.show_home, bg="#333", fg="white").pack()

    # LOGIN SCREEN (BASIC)
    def show_login(self):
        self.clear()

        # Login frame with dark background
        frame = tk.Frame(self.root, bg="#1a1a1a", padx=30, pady=30)
        frame.pack(expand=True)
        tk.Label(frame, text="Login", font=("Poppins", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)

        # Username & Password fields inside show_login()
        tk.Label(frame, text="Username", bg="#1a1a1a", fg="white").pack(anchor="w")
        username = tk.Entry(frame, bg="#222", fg="white", width=50)
        username.pack(fill="x", pady=(0,20))

        tk.Label(frame, text="Password", bg="#1a1a1a", fg="white").pack(anchor="w")
        pass_frame = tk.Frame(frame, bg="#1a1a1a")
        pass_frame.pack(fill="x")
        password = tk.Entry(pass_frame, show="*", bg="#222", fg="white", width=50)
        password.pack(side="left", fill="x", expand=True)

        def toggle(): 
            # Toggle password visibility function for login screen
            password.config(show="" if password.cget("show") == "*" else "*")

        tk.Button(pass_frame, text="👁", command=toggle, bg="#333", fg="white").pack(side="right") # Toggle button

        def login(): # Login function to check credentials against stored data
            with open(DB_FILE, "r") as f:
                data = json.load(f)

            user = data.get(username.get())

            if not user or user["password"] != hash_password(password.get()):
                messagebox.showerror("Error", "Invalid login")
                return

            messagebox.showinfo("Success", "Logged in!")
            # next → go to main menu

        # Login Form Buttons
        tk.Button(frame, text="Login", command=login, bg="red", fg="white").pack(pady=(30, 10)) # Log In
        tk.Button(frame, text="← Back", command=self.show_home, bg="#333", fg="white").pack(pady=(0,10)) # Go Back

# RUN APP
root = tk.Tk()
root.iconbitmap("img_assets/StudyZone.ico")

app = StudyZoneApp(root)
root.mainloop()