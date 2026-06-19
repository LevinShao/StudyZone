import tkinter as tk
from system_functions.backend.ui_helpers import *

from system_functions.custom_trackers.task_tracker import show_task_tracker
from system_functions.custom_trackers.goal_planner import show_goal_planner
from system_functions.custom_trackers.habit_tracker import show_habit_tracker

def show_trackers_menu(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the Productivity Trackers Menu.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Task Tracker", lambda: show_task_tracker(app)).grid(row=0, column=0, padx=30, pady=150)
    create_square(grid, "Goal Planner", lambda: show_goal_planner(app)).grid(row=0, column=1, padx=30, pady=150)
    create_square(grid, "Habit Tracker", lambda: show_habit_tracker(app)).grid(row=0, column=2, padx=30, pady=150)

    bind_exit_menu(app)