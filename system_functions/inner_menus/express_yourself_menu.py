import tkinter as tk
from system_functions.backend.ui_helpers import *

from system_functions.express_yourself.art import art
from system_functions.express_yourself.public_blogs import show_public_blogs

def show_express_menu(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Welcome to the Express Yourself Menu.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Art Pad", lambda: art(app)).grid(row=0, column=0, padx=30, pady=150)
    create_square(grid, "Public Blogs", lambda: show_public_blogs(app)).grid(row=0, column=1, padx=30, pady=150)

    bind_exit_menu(app)