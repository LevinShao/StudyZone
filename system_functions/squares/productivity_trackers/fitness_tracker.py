# WILL WORK ON THIS LATER
import tkinter as tk
from system_functions.backend.ui_helpers import bind_exit_inner_menu

def show_fitness_tracker(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    coming_soon = tk.Label(frame, text="Coming Soon!", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    coming_soon.pack(expand=True)

    # EXIT BUTTON FUNCTIONS
    def exit_btn():
        from system_functions.squares.inner_menus.productivity import show_trackers_menu
        bind_exit_inner_menu(app, show_trackers_menu)

    exit_btn()