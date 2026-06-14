import tkinter as tk

# MAIN COLOUR PALETTE
BG_MAIN = "#0f172a"        # deep navy background
BG_CARD = "#1e293b"        # card background (slightly lighter navy)
ACCENT = "#ef4444"         # red accent (buttons, highlights, etc.)
ACCENT_HOVER = "#dc2626"   # darker red for hover state
TEXT = "#f1f5f9"           # off-white text for high contrast and readability
SUBTLE = "#94a3b8"         # lighter text for subtitles and less important info
INPUT_BG = "#020617"       # very dark background for input fields to make them stand out

def create_small_button(parent, text, command, app, primary=True):
    bg = app.ACCENT if primary else "#22C55E"
    btn = tk.Label(parent, text=text, bg=bg, fg="white", font=("Segoe UI", 12, "bold"), width=18, height=2,cursor="hand2")

    on_enter = lambda e: btn.config(bg="#dc2626" if primary else "#16a34a")
    on_leave = lambda e: btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", lambda e: command())

    return btn

def create_square(app, text, command):
    # Function to create a clickable square for each tool in the main menu
    square = tk.Label(app, text=text, bg=BG_CARD, fg=TEXT, font=("Segoe UI", 14, "bold"), width=20, height=8, cursor="hand2")

    # Hover effect to change background color when mouse is over the square
    hover_on = lambda e: square.config(bg="#334155")
    hover_off = lambda e: square.config(bg=BG_CARD)

    # Bind hover and click events to the square
    square.bind("<Enter>", hover_on)
    square.bind("<Leave>", hover_off)
    square.bind("<Button-1>", lambda e: command())

    return square

# TWO DIFFERENT EXIT BUTTON FUNCTIONS TO AVOID CONFLICTS WITH BINDINGS IN DIFFERENT SCREENS 
# (ESCAPE KEY BINDS TO DIFFERENT FUNCTIONS BASED ON SCREEN)

def bind_exit_menu(app):
    # Exit function to go back to main menu when Escape key is pressed
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16), cursor="hand2")
    exit_btn.place(x=30, y=30)

    def exit_to_menu(event=None):
        app.root.unbind("<Escape>")
        app.show_main_menu()

    hover_on = lambda e: exit_btn.config(bg=ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=ACCENT)

    app.root.bind("<Escape>", exit_to_menu)
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", lambda e: app.show_main_menu())

def bind_exit_home(app):
    # Exit function to go back to home screen (a.k.a first menu) when Escape key is pressed
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16), cursor="hand2")
    exit_btn.place(x=30, y=30)

    def exit_to_home(event=None):
        app.root.unbind("<Escape>")
        app.show_home()

    hover_on = lambda e: exit_btn.config(bg=ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=ACCENT)

    app.root.bind("<Escape>", exit_to_home)
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", lambda e: app.show_home())