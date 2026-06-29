import tkinter as tk
from tkinter import messagebox
from system_functions.backend.ui_helpers import * 

def show_help_menu(self):
    self.clear() 

    # Mainframe setup
    frame = tk.Frame(self.root, bg=self.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Header
    tk.Label(frame, text="Welcome to StudyZone, dear user!", font=("Segoe UI", 30, "bold"), bg=self.BG_CARD, fg=self.TEXT).place(relx=0.5, rely=0.1, anchor="center")

    # Subtitle
    tk.Label(frame, text="What is StudyZone?", font=("Segoe UI", 21, "bold"), bg=self.BG_CARD, fg=self.TEXT).place(relx=0.05, rely=0.2)

    # Body Text
    lorem_text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim"
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                    " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim"
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    
    # Automatically wraps text into a block
    tk.Label(frame, text=lorem_text, font=("Segoe UI", 12), bg=self.BG_CARD, fg=self.TEXT, justify="left", wraplength=1700).place(relx=0.05, rely=0.26)

    tk.Label(frame, text="How does this app work?", font=("Segoe UI", 21, "bold"), bg=self.BG_CARD, fg=self.TEXT).place(relx=0.05, rely=0.4)

    # Body Text
    lorem_text2 = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim"
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                    " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim"
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    
    # Automatically wraps text into a block
    tk.Label(frame, text=lorem_text2, font=("Segoe UI", 12), bg=self.BG_CARD, fg=self.TEXT, justify="left", wraplength=1700).place(relx=0.05, rely=0.46)
    
    bind_exit_home(self)