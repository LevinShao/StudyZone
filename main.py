import tkinter as tk                # GUI library for application interface
from tkinter import messagebox      # For showing pop-up messages
import json                         # Data storage
import os                           # File handling
import random                       # For random motivational messages
from datetime import datetime       # Time detection
from PIL import Image, ImageTk      # Logo
import pygame                       # Music player + playlist system (Using Pygame since Tkinter does not support music functionality natively)

# INTEGRATION OF FUNCTIONALITY MODULES
from system_functions.user_profile_dashboard import show_profile_menu            # User Profile Dashboard module
from system_functions.streak_menu import show_streak_menu                        # Streak Tracking module
from system_functions.registration_login_systems import *                        # Registration & Login systems
from system_functions.music_system.music_settings import show_music_player       # Music Player module
from system_functions.notebook import show_notebook                              # Digital Notebook module
from system_functions.calendar.calendar_view import show_calendar                # Calendar + Reminders systems
from system_functions.flashcards.flashcards_main import show_flashcards          # Flashcards module
from system_functions.pomodoro_timer import show_pomodoro_timer                  # Pomodoro Timer module
from system_functions.file_storage import show_file_storage
from system_functions.support import show_support_menu
from system_functions.backend.ui_helpers import *                                # Import everything from UI helpers module

from system_functions.inner_menus.custom_trackers import show_trackers_menu      # Custom Trackers Menu
from system_functions.inner_menus.skill_training_menu import show_skill_menu     # Skill Training Menu
from system_functions.inner_menus.express_yourself_menu import show_express_menu # Express Yourself Menu

# UTILITY FUNCTION TO CREATE STYLED INPUT FIELDS WITH LABELS AND ERROR MESSAGES
def create_field(parent, label, is_password=False):
    # Field label (aligned to the left)
    tk.Label(parent, text=label, bg=BG_CARD, fg=TEXT).pack(anchor="w")

    # Input wrapper to hold the entry and optional password toggle button
    # Ensures consistent spacing even when toggle is not present
    wrapper = tk.Frame(parent, bg=BG_CARD)
    wrapper.pack(fill="x", pady=(6, 0))

    # Input field with padding and expansion to fill available space
    entry = tk.Entry(wrapper, bg=INPUT_BG, fg=TEXT, insertbackground="white", relief="flat", font=("Segoe UI", 12),
                     highlightbackground=TEXT, highlightthickness=1, width=45, show="*" if is_password else "")
    entry.pack(side="left", fill="x", expand=True, ipadx=10)

    if is_password:
        # If this is a password field, add a toggle button to show/hide the password
        def toggle():
            # Toggle between showing and hiding the password characters
            # Works by checking the current "show" configuration of the entry widget
            entry.config(show="" if entry.cget("show") == "*" else "*")

        tk.Button(wrapper, text="👁", command=toggle, bg="#334155", fg=TEXT, relief="flat", width=4).pack(side="right", padx=5)

    error = tk.Label(parent, text="", fg="#ef4444", bg=BG_CARD, font=("Arial", 8))
    error.pack(anchor="w", pady=(5, 15))

    # Return the entry widget and the error label for validation feedback
    return entry, error

# UTILITY FUNCTION TO CREATE STYLED BUTTONS
def create_button(parent, text, command, primary=True):
    bg = ACCENT if primary else BG_CARD # Primary buttons are red, secondary are card-colored
    btn = tk.Label(parent, text=text, bg=bg, fg="white", font=("Segoe UI", 16, "bold"), width=22, height=2, cursor="hand2")

    hover_on = lambda e: btn.config(bg=ACCENT_HOVER if primary else "#334155") # Change background on hover
    hover_off = lambda e: btn.config(bg=bg)

    btn.bind("<Enter>", hover_on) # Bind hover events to change button color
    btn.bind("<Leave>", hover_off) # Bind leave event to revert button color
    btn.bind("<Button-1>", lambda e: command()) # Bind click event to execute the provided command function

    return btn # Return the styled button widget

# APP CLASS
class StudyZoneApp:
    def __init__(self, root):
        # Initialize the main application class, set up the root window, and show the home screen
        self.current_user = None
        self.root = root
        self.root.title("StudyZone")
        self.root.state("zoomed")
        self.root.configure(bg="#111111")

        # Colour scheme initialization
        self.BG_MAIN = BG_MAIN
        self.BG_CARD = BG_CARD
        self.ACCENT = ACCENT
        self.ACCENT_HOVER = ACCENT_HOVER
        self.TEXT = TEXT
        self.SUBTLE = SUBTLE

        # UI helper functions
        self.create_field = create_field
        self.create_square = create_square
        self.say_hello = ["Welcome to StudyZone", "Hello", "Nice to meet you", "Hey there"]
        self.main_msg = random.choice(self.say_hello)

        # Initialize music system
        pygame.mixer.init()

        # Default music settings
        self.current_song = "system_functions/music_system/Creo - Flow.mp3"
        self.playlist = ["system_functions/music_system/Creo - Flow.mp3"]
        self.volume = 0.5

        pygame.mixer.music.set_volume(self.volume)

        # Dynamic time-based emoji in welcome message
        current_hour = datetime.now().hour # Current Time

        if 5 <= current_hour < 12:
            self.time_emoji = "🌅"      # Dawn / Morning
        elif 12 <= current_hour < 18:
            self.time_emoji = "☀️"      # Day / Afternoon
        elif 18 <= current_hour < 22:
            self.time_emoji = "🌆"      # Dusk / Evening
        else:
            self.time_emoji = "🌙"      # Night / Midnight

        self.show_home()

    # CLEAR SCREEN
    def clear(self):
        self.root.unbind("<Escape>")

        for widget in self.root.winfo_children():
            widget.destroy()

    def play_music(self, song=None):
        # Load and play music using Pygame mixer, with error handling for missing files
        if song:
            self.current_song = song

        if not self.playlist: # If playlist is empty, add the default song to prevent errors
            return

        try:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play(-1)  # loop forever
        except:
            print("Music file missing:", self.current_song)

    def dev_login(self):
        # Deverloper mode for quick access without registration/login during development
        # Will be remade into an app help guide in the future
        username = "StudyDev"

        # Load DB
        with open(ACCOUNTDB_FILE, "r") as f:
            data = json.load(f)

        # Create account if it doesn't exist
        if username not in data:
            data[username] = {
                "username": username,
                "email": "dev@studyzone.com",
                "dob": "2000-01-01",
                "password": hash_password("Password123!"),
                "streak": 0
            }

            with open(ACCOUNTDB_FILE, "w") as f:
                json.dump(data, f, indent=4)

        # Log in directly
        self.current_user = username
        update_login_streak(username)
        self.show_main_menu()
        self.play_music()

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
            # Load and display the logo image at the top of the home screen
            img = Image.open(logo_path)
            img = img.resize((1000, 230))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self.logo_img, bg=BG_MAIN).pack()

        # SUBTITLE
        tk.Label(container, text="FOCUS, BUILD, IMPROVE.", font=("Segoe UI", 30), fg=SUBTLE, bg=BG_MAIN).pack(pady=0.1)

        # BUTTONS LOWER
        button_frame = tk.Frame(container, bg=BG_MAIN)
        button_frame.pack(pady=100)

        create_button(button_frame, "Register", lambda: user_registration(self)).pack(pady=10)
        create_button(button_frame, "Log In", lambda: user_login(self)).pack(pady=20)
        create_button(button_frame, "Developer Mode", self.dev_login, primary=False).pack(pady=10)

        def confirm_exit(event=None):
            # Exit confirmation popup when user presses Escape key in the main menu
            response = messagebox.askyesno("Exit", "Do you want to close StudyZone?")
            if response:
                self.root.destroy() # Self-destruct upon confirmation

        self.root.bind("<Escape>", confirm_exit)

    def show_main_menu(self):
        self.clear()
        self.root.configure(bg=BG_MAIN)

        # MOTIVATIONAL MESSAGES. RANDOMLY SELECTED FROM messages.md
        try:
            with open("system_messages/messages.md", "r", encoding="utf-8") as f:
                # Reads lines, strips whitespace, removes empty lines
                messages = [line.strip() for line in f if line.strip()]
                message = random.choice(messages)
        except FileNotFoundError:
            # Fallback message if messages.md is missing for whatever reason
            message = "Focus on your goals."

        # Container for welcome message and tool grid
        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True)

        # Welcome Message with dynamic emoji based on time of day
        welcome_frame = tk.Frame(container, bg=BG_MAIN)
        welcome_frame.pack(pady=(60, 45))

        # Use grid layout for welcome message to allow emoji and text to be aligned nicely
        row_frame = tk.Frame(welcome_frame, bg=BG_MAIN)
        row_frame.pack()

        tk.Label(row_frame, text=self.time_emoji, font=("Segoe UI", 70), fg=TEXT, bg=BG_MAIN).grid(row=0, column=0, rowspan=2, padx=(0, 12))
        tk.Label(row_frame, text=f"{self.main_msg}, {self.current_user}", font=("Segoe UI", 30, "bold"), fg=TEXT, bg=BG_MAIN).grid(row=0, column=1, sticky="w")
        tk.Label(row_frame, text=message, font=("Segoe UI", 20), fg=SUBTLE, bg=BG_MAIN).grid(row=1, column=1, sticky="w")

        # TOOL GRID
        grid = tk.Frame(container, bg=BG_MAIN)
        grid.pack(pady=0.1)
        
        def confirm_exit(event=None):
            # Exit confirmation popup when user presses Escape key in the main menu
            response = messagebox.askyesno("Exit", "Do you want to close StudyZone?")
            if response:
                self.root.destroy() # Self-destruct upon confirmation

        self.root.bind("<Escape>", confirm_exit)

        # MAIN MENU SQUARES
        create_square(grid, "Custom Trackers", lambda: show_trackers_menu(self)).grid(row=0, column=1, padx=20, pady=20)
        create_square(grid, "Digital Notebook", lambda: show_notebook(self)).grid(row=0, column=2, padx=20, pady=20)
        create_square(grid, "Calendar", lambda: show_calendar(self)).grid(row=0, column=3, padx=20, pady=20)
        create_square(grid, "Flashcards", lambda: show_flashcards(self)).grid(row=0, column=4, padx=20, pady=20)
        create_square(grid, "Pomodoro Timer", lambda: show_pomodoro_timer(self)).grid(row=0, column=5, padx=20, pady=20)
        create_square(grid, "Skill Trainers", lambda: show_skill_menu(self)).grid(row=1, column=1, padx=20, pady=50)
        create_square(grid, "Express Yourself", lambda: show_express_menu(self)).grid(row=1, column=2, padx=20, pady=50)
        create_square(grid, "File Storage", lambda: show_file_storage(self)).grid(row=1, column=3, padx=20, pady=50)

        # USER PROFILE BUTTON
        canvas2 = tk.Canvas(self.root, width=100, height=100, bg=BG_MAIN, highlightthickness=0)
        canvas2.place(relx=0.97, rely=0.95, anchor="se")
        canvas2.create_oval(5, 5, 100, 100, fill=ACCENT, outline="")
        canvas2.create_text(54, 50, text="👤", fill="white", font=("Segoe UI", 30))

        hover_on = lambda e: canvas2.itemconfig(1, fill=ACCENT_HOVER) # Change oval color on hover
        hover_off = lambda e: canvas2.itemconfig(1, fill=ACCENT) # Revert oval color when not hovering

        canvas2.bind("<Enter>", hover_on)
        canvas2.bind("<Leave>", hover_off)
        canvas2.bind("<Button-1>", lambda e: show_profile_menu(self))

        # MUSIC PLAYER BUTTON
        canvas1 = tk.Canvas(self.root, width=100, height=100, bg=BG_MAIN, highlightthickness=0)
        canvas1.place(relx=0.97, rely=0.83, anchor="se")
        canvas1.create_oval(5, 5, 100, 100, fill=ACCENT, outline="")
        canvas1.create_text(50, 50, text="🎵", fill="white", font=("Segoe UI", 30))

        hover_on = lambda e: canvas1.itemconfig(1, fill=ACCENT_HOVER) # Change oval color on hover
        hover_off = lambda e: canvas1.itemconfig(1, fill=ACCENT) # Revert oval color when not hovering

        canvas1.bind("<Enter>", hover_on)
        canvas1.bind("<Leave>", hover_off)
        canvas1.bind("<Button-1>", lambda e: show_music_player(self))

        # STREAK BUTTON
        canvas3 = tk.Canvas(self.root, width=100, height=100, bg=BG_MAIN, highlightthickness=0)
        canvas3.place(relx=0.97, rely=0.71, anchor="se")
        canvas3.create_oval(5, 5, 100, 100, fill=ACCENT, outline="")
        canvas3.create_text(50, 50, text="🔥", fill="white", font=("Segoe UI", 30))

        hover_on = lambda e: canvas3.itemconfig(1, fill=ACCENT_HOVER) # Change oval color on hover
        hover_off = lambda e: canvas3.itemconfig(1, fill=ACCENT) # Revert oval color when not hovering

        canvas3.bind("<Enter>", hover_on)
        canvas3.bind("<Leave>", hover_off)
        canvas3.bind("<Button-1>", lambda e: show_streak_menu(self))

        # SUPPORT BUTTON
        canvas4 = tk.Canvas(self.root, width=100, height=100, bg=BG_MAIN, highlightthickness=0)
        canvas4.place(relx=0.03, rely=0.95, anchor="sw")
        canvas4.create_rectangle(5, 5, 100, 100, fill=ACCENT, outline="")
        canvas4.create_text(50, 50, text="📩", fill="white", font=("Segoe UI", 30))

        hover_on = lambda e: canvas4.itemconfig(1, fill=ACCENT_HOVER) # Change oval color on hover
        hover_off = lambda e: canvas4.itemconfig(1, fill=ACCENT) # Revert oval color when not hovering

        canvas4.bind("<Enter>", hover_on)
        canvas4.bind("<Leave>", hover_off)
        canvas4.bind("<Button-1>", lambda e: show_support_menu(self))

# RUN APP
root = tk.Tk()
root.iconbitmap("img_assets/StudyZone.ico")
app = StudyZoneApp(root)
root.mainloop()