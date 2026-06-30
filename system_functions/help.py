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
    txt = (
            "StudyZone is an all-in-one productivity application designed to help students stay organised, focused and motivated. Instead of switching between multiple "
            "applications, StudyZone brings essential study tools together into one desktop program.\n\n"

            "The application includes productivity trackers, digital study tools, skill training exercises, wellbeing features and account management systems. Every "
            "feature is designed to reduce distractions, make studying more efficient, and make yourself better than ever, "
            "whether you are preparing for exams, completing homework or simply organising your daily routine."
            )
    
    # Automatically wraps text into a block
    tk.Label(frame, text=txt, font=("Segoe UI", 12), bg=self.BG_CARD, fg=self.TEXT, justify="left", wraplength=1700).place(relx=0.05, rely=0.26)

    tk.Label(frame, text="How does this app work?", font=("Segoe UI", 21, "bold"), bg=self.BG_CARD, fg=self.TEXT).place(relx=0.05, rely=0.4)

    # Body Text
    txt2 = (
            "Once you create an account and log in, your personal data is stored locally on your computer and automatically loaded each time you use the application. "
            "StudyZone remembers your tasks, notes, flashcards, goals, habits and other information so you can continue where you left off.\n\n"

            "Navigate through the application using the coloured squares and circular buttons on the main dashboard. Each section focuses on a different aspect of "
            "productivity, including study tools, habit building, wellbeing, creativity and skill development. Most screens can be exited quickly by pressing the "
            "Escape key or using the back button in the top-left corner."
            )
    
    # Automatically wraps text into a block
    tk.Label(frame, text=txt2, font=("Segoe UI", 12), bg=self.BG_CARD, fg=self.TEXT, justify="left", wraplength=1700).place(relx=0.05, rely=0.46)

    okbtn = create_small_button(frame, "Got it, thanks!", self.show_home, self, primary=True)
    okbtn.config(width=40, height=5)
    okbtn.place(relx=0.5, rely=0.95, anchor="s")
    
    bind_exit_home(self)