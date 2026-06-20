import tkinter as tk
from system_functions.backend.ui_helpers import *

from system_functions.squares.study_tools.notebook.create_new_page import create_new_page
from system_functions.squares.study_tools.flashcards.flashcards_main import show_flashcards
from system_functions.squares.study_tools.pomodoro_timer import show_pomodoro_timer
from system_functions.squares.study_tools.calculator import show_calculator

def show_studymenu(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the StudyMenu.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Digital Notebook", lambda: create_new_page(app)).grid(row=0, column=0, padx=30, pady=150)
    create_square(grid, "Flashcards", lambda: show_flashcards(app)).grid(row=0, column=1, padx=30, pady=150)
    create_square(grid, "Pomodoro Timer", lambda: show_pomodoro_timer(app)).grid(row=0, column=2, padx=30, pady=150)
    create_square(grid, "Calculator", lambda: show_calculator(app)).grid(row=0, column=3, padx=30, pady=150)

    bind_exit_menu(app)