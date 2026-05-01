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

# MAIN COLOUR PALETTE
BG_MAIN = "#0f172a"        # deep navy background
BG_CARD = "#1e293b"        # card background (slightly lighter navy)
ACCENT = "#ef4444"         # red accent (buttons, highlights, etc.)
ACCENT_HOVER = "#dc2626"   # darker red for hover state
TEXT = "#f1f5f9"           # off-white text for high contrast and readability
SUBTLE = "#94a3b8"         # lighter text for subtitles and less important info
INPUT_BG = "#020617"       # very dark background for input fields to make them stand out

# ENSURE DATABASE FILE EXISTS
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

# UTILITY FUNCTION TO CREATE STYLED BUTTONS
def create_button(parent, text, command, primary=True):
    bg = ACCENT if primary else BG_CARD # Primary buttons are red, secondary are card-colored

    btn = tk.Label(parent, text=text, bg=bg, fg="white", font=("Segoe UI", 16, "bold"), width=22, height=2, cursor="hand2")

    def on_enter(e): 
        # Change background on cursor hover (darker red for primary, slightly lighter for secondary)
        btn.config(bg=ACCENT_HOVER if primary else "#334155")

    def on_leave(e): 
        # Revert background when cursor is not hovering
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter) # Bind hover events to change button color
    btn.bind("<Leave>", on_leave) # Bind leave event to revert button color
    btn.bind("<Button-1>", lambda e: command()) # Bind click event to execute the provided command function

    return btn # Return the styled button widget

# UTILITY FUNCTION TO CREATE STYLED INPUT FIELDS WITH LABELS AND ERROR MESSAGES
def create_field(parent, label, is_password=False):
    tk.Label(parent, text=label, bg=BG_CARD, fg=TEXT).pack(anchor="w") # Field label (aligned to the left)

    # Input wrapper to hold the entry and optional password toggle button
    # Ensures consistent spacing even when toggle is not present
    wrapper = tk.Frame(parent, bg=BG_CARD)
    wrapper.pack(fill="x", pady=10)

    entry = tk.Entry(wrapper, bg=INPUT_BG, fg=TEXT, insertbackground="white", relief="flat", font=("Segoe UI", 12), 
                     highlightbackground=TEXT, highlightthickness=1, width=45, show="*" if is_password else "")
    
    entry.pack(side="left", fill="x", expand=True, ipadx=10) # Input field with padding and expansion to fill available space

    if is_password: # If this is a password field, add a toggle button to show/hide the password
        def toggle():
            entry.config(show="" if entry.cget("show") == "*" else "*")

        tk.Button(wrapper, text="👁", command=toggle, bg="#334155", fg=TEXT, relief="flat", width=4).pack(side="right", padx=5)

    error = tk.Label(parent, text="", fg="#ef4444", bg=BG_CARD, font=("Arial", 8))
    error.pack(anchor="w")

    return entry, error # Return the entry widget and the error label for validation feedback

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
        self.clear() # Clear existing widgets to show home screen
        self.root.configure(bg=BG_MAIN) # Set background color for home screen

        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(expand=True)

        # LOGO
        logo_frame = tk.Frame(container, bg=BG_MAIN)
        logo_frame.pack(pady=100)

        logo_path = os.path.join(os.path.dirname(__file__), "img_assets/StudyZone.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((1000, 230))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self.logo_img, bg=BG_MAIN).pack()

        # SUBTITLE
        tk.Label(container, text="FOCUS, BUILD, IMPROVE.", font=("Segoe UI", 30), fg=SUBTLE, bg=BG_MAIN).pack(pady=0.1)

        # BUTTONS LOWER
        button_frame = tk.Frame(container, bg=BG_MAIN)
        button_frame.pack(pady=100)

        create_button(button_frame, "Register", self.show_register).pack(pady=10)
        create_button(button_frame, "Log In", self.show_login, primary=False).pack(pady=20)

    # REGISTER SCREEN
    def show_register(self):
        self.clear()

        # Registration frame, dark background
        outer = tk.Frame(self.root, bg=BG_MAIN)
        outer.pack(expand=True)

        frame = tk.Frame(outer, bg=BG_CARD, padx=100, pady=40)
        frame.pack()

        tk.Label(frame, text="Register", font=("Segoe UI", 26, "bold"), bg=BG_CARD, fg=TEXT).pack(pady=10)

        username, err_username = create_field(frame, "Username") # Username field with error label
        email, err_email = create_field(frame, "Email") # Email field with error label
        dob, err_dob = create_field(frame, "Date of Birth (YYYY-MM-DD)") # DOB field with error label)
        password, err_pass = create_field(frame, "Password", is_password=True)

        general_error = tk.Label(frame, text="", fg="red", bg=BG_CARD)
        general_error.pack() # General error (e.g. user already exists)

        # VALIDATION MECHANISM
        def validate():
            valid = True # Assume valid until checks fail

            # USERNAME
            if username.get().strip() == "": # Check if username is empty
                err_username.config(text="Username required")
                valid = False
            elif len(username.get()) < 3: # Check if username is too short
                err_username.config(text="Username too short")
                valid = False
            elif len(username.get()) > 20: # Check if username is too long
                err_username.config(text="Username too long")
                valid = False
            elif not re.match(r"^[a-zA-Z0-9_]+$", username.get()): # Check if username contains invalid characters
                err_username.config(text="Only letters, numbers, _")
                valid = False
            else:
                err_username.config(text="")

            # EMAIL
            if not validate_email(email.get()): # Check if email is valid
                err_email.config(text="Invalid email")
                valid = False
            else:
                err_email.config(text="")

            # DOB
            if not validate_dob(dob.get()): # Check if DOB is valid
                err_dob.config(text="Invalid DOB")
                valid = False
            else:
                err_dob.config(text="")

            # PASSWORD
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
        submit_btn = tk.Button(frame, text="Submit", state="disabled", command=submit, bg=ACCENT, fg=TEXT, width=20, height=2)
        submit_btn.pack(pady=10)

        tk.Button(frame, text="← Back", command=self.show_home, bg=BG_CARD, fg=TEXT, width=20, height=2).pack(pady=10) # Go Back button

    # LOGIN SCREEN (BASIC)
    def show_login(self):
        self.clear()

        # SAME OUTER STRUCTURE AS REGISTER
        outer = tk.Frame(self.root, bg=BG_MAIN)
        outer.pack(expand=True)

        frame = tk.Frame(outer, bg=BG_CARD, padx=100, pady=40)
        frame.pack()

        tk.Label(frame, text="Login",
                font=("Segoe UI", 26, "bold"),
                bg=BG_CARD, fg=TEXT).pack(pady=10)

        # INPUT FIELDS
        username, _ = create_field(frame, "Username")
        password, _ = create_field(frame, "Password", is_password=True)

        general_error = tk.Label(frame, text="", fg="red", bg=BG_CARD)
        general_error.pack()

        # LOGIN LOGIC
        def login():
            with open(DB_FILE, "r") as f:
                data = json.load(f)

            input_username = username.get() # Get the input username for case-insensitive comparison
            user = None

            for existing_user in data: # Loop through existing users to find a case-insensitive match
                if existing_user.lower() == input_username.lower():
                    user = data[existing_user]
                    break

            if not user or user["password"] != hash_password(password.get()): 
                # Check if user exists and password matches
                general_error.config(text="Invalid username or password")
                return

            messagebox.showinfo("Success", f"Welcome {user['username']}!")

        # BUTTONS
        tk.Button(frame, text="Login", command=login, bg=ACCENT, fg=TEXT, width=20, height=2).pack(pady=10)
        tk.Button(frame, text="← Back", command=self.show_home, bg=BG_CARD, fg=TEXT, width=20, height=2).pack(pady=10)

# RUN APP
root = tk.Tk()
root.iconbitmap("img_assets/StudyZone.ico")

app = StudyZoneApp(root)
root.mainloop()