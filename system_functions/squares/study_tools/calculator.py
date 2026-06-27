# Special thanks to geeksforgeeks.org for providing the tutorial for this function
import tkinter as tk
from system_functions.backend.ui_helpers import bind_exit_inner_menu

def show_calculator(app):
    app.clear()

    expression = "" # Expression means the current expression being calculated
    display = tk.StringVar() # Display means the current display on the calculator, updates as the user types

    container = tk.Frame(app.root, bg=app.BG_MAIN)
    container.pack(fill="both", expand=True)

    card = tk.Frame(container, bg=app.BG_CARD, padx=30, pady=30)
    card.pack(expand=True)

    tk.Label(card, text="Calculator", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT).grid(row=0, column=0, columnspan=4, pady=(0,20))
    entry = tk.Entry(card, textvariable=display, font=("Segoe UI", 14), justify="right")
    entry.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0,15), ipady=8)

    def press(key):
        nonlocal expression
        expression += str(key) # Add the key to the expression
        display.set(expression) # Update the display with the expression

    def equal():
        nonlocal expression
        
        try:
            result = str(eval(expression)) # Evaluate the expression using eval
            display.set(result) # Update the display with the result
            expression = result
        except:
            display.set("Error") # Error message
            expression = ""

    def clear():
        nonlocal expression
        expression = "" # Clear the expression
        display.set("") # Clear the display

    def make_button(text, row, column, command):
        # Adds a button for every single number and operator
        tk.Button(card, text=text, command=command, width=8, height=2, bg="#334155", fg="white", relief="flat").grid(row=row, column=column, padx=3, pady=3)

    # Numbers
    make_button("1", 2, 0, lambda: press(1)) # Text = 1, Row = 2, Column = 0, Command = press(1)
    make_button("2", 2, 1, lambda: press(2)) # Text = 2, Row = 2, Column = 1, Command = press(2)...
    make_button("3", 2, 2, lambda: press(3)) # etc etc etc
    make_button("4", 3, 0, lambda: press(4))
    make_button("5", 3, 1, lambda: press(5))
    make_button("6", 3, 2, lambda: press(6))
    make_button("7", 4, 0, lambda: press(7))
    make_button("8", 4, 1, lambda: press(8))
    make_button("9", 4, 2, lambda: press(9))
    make_button("0", 5, 0, lambda: press(0))
    make_button(".", 5, 1, lambda: press("."))

    # Operators
    make_button("+", 2, 3, lambda: press("+"))
    make_button("-", 3, 3, lambda: press("-"))
    make_button("×", 4, 3, lambda: press("*"))
    make_button("÷", 5, 3, lambda: press("/"))

    # Bottom row
    make_button("Clear", 6, 0, clear) # Text = Clear, Row = 6, Column = 0, Command = clear
    make_button("=", 6, 1, equal) # Text = =, Row = 6, Column = 1, Command = equal

    # EXIT BUTTON FUNCTIONS
    def exit_btn():
        from system_functions.squares.inner_menus.study_tools import show_studymenu
        bind_exit_inner_menu(app, show_studymenu)

    exit_btn()