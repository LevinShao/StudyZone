import tkinter as tk

# MAIN COLOUR PALETTE
BG_MAIN = "#0f172a"        # deep navy background
BG_CARD = "#1e293b"        # card background (slightly lighter navy)
ACCENT = "#ef4444"         # red accent (buttons, highlights, etc.)
ACCENT_HOVER = "#dc2626"   # darker red for hover state
TEXT = "#f1f5f9"           # off-white text for high contrast and readability
SUBTLE = "#94a3b8"         # lighter text for subtitles and less important info
INPUT_BG = "#020617"       # very dark background for input fields to make them stand out

def create_small_button(app, text, command, primary=True):
    bg = app.ACCENT if primary else "#22C55E"
    btn = tk.Label(app, text=text, bg=bg, fg="white", font=("Segoe UI", 12, "bold"), width=18, height=2,cursor="hand2")

    def on_enter(e):
        # Change button color on hover
        btn.config(bg="#dc2626" if primary else "#16a34a")

    def on_leave(e):
        # Revert button color when not hovering
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", lambda e: command())

    return btn

def create_square(app, text, command):
    # Function to create a clickable square for each tool in the main menu
    square = tk.Label(app, text=text, bg=BG_CARD, fg=TEXT, font=("Segoe UI", 14, "bold"), width=20, height=8, cursor="hand2")

    # Hover effect to change background color when mouse is over the square
    def hover_on(e): 
        square.config(bg="#334155")

    def hover_off(e): 
        square.config(bg=BG_CARD)

    # Bind hover and click events to the square
    square.bind("<Enter>", hover_on)
    square.bind("<Leave>", hover_off)
    square.bind("<Button-1>", lambda e: command())

    return square

def create_field(app, label, is_password=False):
    # UTILITY FUNCTION TO CREATE STYLED INPUT FIELDS WITH LABELS AND ERROR MESSAGES
    tk.Label(app, text=label, bg=app.BG_CARD, fg=app.TEXT).pack(anchor="w") # Field label (aligned to the left)

    # Input wrapper to hold the entry and optional password toggle button
    # Ensures consistent spacing even when toggle is not present
    wrapper = tk.Frame(app, bg=app.BG_CARD)
    wrapper.pack(fill="x", pady=(6, 0))

    entry = tk.Entry(wrapper, bg=app.INPUT_BG, fg=app.TEXT, insertbackground="white", relief="flat", font=("Segoe UI", 12), 
                     highlightbackground=app.TEXT, highlightthickness=1, width=45, show="*" if is_password else "")
    entry.pack(side="left", fill="x", expand=True, ipadx=10) # Input field with padding and expansion to fill available space

    if is_password: # If this is a password field, add a toggle button to show/hide the password
        def toggle():
            entry.config(show="" if entry.cget("show") == "*" else "*")

        tk.Button(wrapper, text="👁", command=toggle, bg="#334155", fg=app.TEXT, relief="flat", width=4).pack(side="right", padx=5)

    error = tk.Label(app, text="", fg="#ef4444", bg=app.BG_CARD, font=("Arial", 8))
    error.pack(anchor="w", pady=(0, 2))

    return entry, error # Return the entry widget and the error label for validation feedback

# TWO DIFFERENT EXIT BUTTON FUNCTIONS TO AVOID CONFLICTS WITH BINDINGS IN DIFFERENT SCREENS 
# (ESCAPE KEY BINDS TO DIFFERENT FUNCTIONS BASED ON SCREEN)

def bind_exit_menu(app):
    # Exit function to go back to main menu when Escape key is pressed
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16), cursor="hand2")
    exit_btn.place(x=30, y=30)

    def exit_to_menu(event=None):
        app.root.unbind("<Escape>")
        app.show_main_menu()

    def hover_on(e): 
        exit_btn.config(bg=ACCENT_HOVER)

    def hover_off(e): 
        exit_btn.config(bg=ACCENT)

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

    def hover_on(e): 
        exit_btn.config(bg=ACCENT_HOVER)

    def hover_off(e): 
        exit_btn.config(bg=ACCENT)

    app.root.bind("<Escape>", exit_to_home)
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", lambda e: app.show_home())