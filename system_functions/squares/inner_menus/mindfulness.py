import tkinter as tk
from system_functions.backend.ui_helpers import *
from system_functions.squares.mindfulness.wellbeing_journal import journal

def show_mindfulness(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the Mindfulness Portal.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Wellbeing Journal", lambda: journal(app)).grid(row=0, column=0, padx=30, pady=150)

    bind_exit_menu(app)