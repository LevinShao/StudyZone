import tkinter as tk

# --------------------- MAIN COLOUR PALETTE ---------------------

BG_MAIN = "#0f172a"        # deep navy background
BG_CARD = "#1e293b"        # card background (slightly lighter navy)
ACCENT = "#ef4444"         # red accent (buttons, highlights, etc.)
ACCENT_HOVER = "#dc2626"   # darker red for hover state
TEXT = "#f1f5f9"           # off-white text for high contrast and readability
SUBTLE = "#94a3b8"         # lighter text for subtitles and less important info
INPUT_BG = "#020617"       # very dark background for input fields to make them stand out

# --------------------- CREATE UI HELPER FUNCTIONS --------------------- 

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

def create_oval(app, x, y, emoji, command):
    canvas = tk.Canvas(app, width=100, height=100, bg=BG_MAIN, highlightthickness=0, cursor="hand2")
    canvas.place(relx=x, rely=y, anchor="se")
    oval = canvas.create_oval(5, 5, 100, 100, fill=ACCENT, outline="")
    canvas.create_text(50, 50, text=emoji, fill="white", font=("Segoe UI", 30))

    hover_on = lambda e: canvas.itemconfig(oval, fill=ACCENT_HOVER)
    hover_off = lambda e: canvas.itemconfig(oval, fill=ACCENT)

    canvas.bind("<Enter>", hover_on)
    canvas.bind("<Leave>", hover_off)
    canvas.bind("<Button-1>", lambda event: command())

    return canvas

# --------------------- EXIT BINDS ---------------------

# THREE DIFFERENT EXIT BUTTON FUNCTIONS TO AVOID CONFLICTS WITH BINDINGS IN DIFFERENT SCREENS 
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

def bind_exit_inner_menu(app, destination):
    def exit_to_inner_menu(event=None):
        app.root.unbind("<Escape>")
        destination(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_inner_menu)
    app.root.bind("<Escape>", exit_to_inner_menu)

# --------------------- SCROLLABLE PAGE! (EXPERIMENTAL) ---------------------

def create_scrollable_page(root, bg):
    # This is a debugging tool used to fix issues with StudyZone display when users use the app on computers with extremely small screens
    canvas = tk.Canvas(root, bg=bg, highlightthickness=0) # Create a canvas widget to hold the scrollable frame

    def _on_mousewheel(event):
        # Check if the canvas widget still exists in the DOM because sometimes it gets destroyed
        if canvas.winfo_exists():
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") # Scroll the canvas up or down based on the mouse wheel delta

    # Add a scrollbar to the canvas to allow vertical scrolling
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) # Update the scroll region when the scrollable frame changes size

    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") # Create a window to hold the scrollable frame

    def resize(event):
        # Update the window width when the canvas changes size
        canvas.itemconfigure(window, width=event.width)

    canvas.bind("<Configure>", resize)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    return scrollable_frame, canvas # Return the scrollable frame and canvas widget