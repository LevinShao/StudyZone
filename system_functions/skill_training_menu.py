import tkinter as tk
from system_functions.backend.ui_helpers import *

from system_functions.skill_testers.aim_trainer import show_aim_trainer
from system_functions.skill_testers.reaction_trainer import test3
from system_functions.skill_testers.memory_trainer import test2

def show_skill_menu(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the Skill Training Menu.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Aim Trainer", lambda: show_aim_trainer(app)).grid(row=0, column=1, padx=50, pady=150)
    create_square(grid, "Reaction Trainer", lambda: test2(app)).grid(row=0, column=2, padx=50, pady=150)
    create_square(grid, "Memory Trainer", lambda: test3(app)).grid(row=0, column=3, padx=50, pady=150)

    bind_exit_menu(app)