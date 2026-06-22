import tkinter as tk
from system_functions.backend.ui_helpers import *
from system_functions.squares.utilities.spin_a_wheel import spin_a_wheel
from system_functions.squares.utilities.flip_a_coin import coinflip

def show_utilities(app):
    app.clear()

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Some of these are hella useful.", font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=100)

    # TOOL GRID
    grid = tk.Frame(container, bg=BG_MAIN)
    grid.pack(pady=0.1)

    create_square(grid, "Spin a Wheel", lambda: spin_a_wheel(app)).grid(row=0, column=0, padx=30, pady=150)
    create_square(grid, "Coin Flipper", lambda: coinflip(app)).grid(row=0, column=1, padx=30, pady=150)

    bind_exit_menu(app)