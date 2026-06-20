# WILL WORK ON THIS LATER
import tkinter as tk
from system_functions.backend.ui_helpers import *

def show_fitness_tracker(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    coming_soon = tk.Label(frame, text="Coming Soon!", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    coming_soon.pack(expand=True)

    # EXIT BUTTON FUNCTIONS
    def exit_to_trackers_menu(event=None):
        from system_functions.squares.inner_menus.productivity import show_trackers_menu

        app.root.unbind("<Escape>")
        show_trackers_menu(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_trackers_menu)
    app.root.bind("<Escape>", exit_to_trackers_menu)
