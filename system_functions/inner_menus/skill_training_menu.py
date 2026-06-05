import tkinter as tk
from system_functions.backend.ui_helpers import *

from system_functions.skill_testers.aim_trainer import show_aim_trainer
from system_functions.skill_testers.reaction_trainer import show_reaction_trainer
from system_functions.skill_testers.memory_trainer import show_memory_trainer
from system_functions.skill_testers.typing_speed import show_typing_app
from system_functions.skill_testers.cps_counter import show_cps_counter

def show_skill_menu(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the Skill Training Menu.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Aim Trainer", lambda: show_aim_trainer(app)).grid(row=0, column=1, padx=30, pady=150)
    create_square(grid, "Reaction Time", lambda: show_reaction_trainer(app)).grid(row=0, column=2, padx=30, pady=150)
    create_square(grid, "Memory Trainer", lambda: show_memory_trainer(app)).grid(row=0, column=3, padx=30, pady=150)
    create_square(grid, "Typing Speed", lambda: show_typing_app(app)).grid(row=0, column=4, padx=30, pady=150)
    create_square(grid, "CPS Counter", lambda: show_cps_counter(app)).grid(row=0, column=5, padx=30, pady=150)

    bind_exit_menu(app)