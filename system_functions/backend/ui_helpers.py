import tkinter as tk

def create_small_button(parent, text, command, app, primary=True):
    bg = app.ACCENT if primary else "#22C55E"
    btn = tk.Label(parent, text=text, bg=bg, fg="white", font=("Segoe UI", 12, "bold"), width=18, height=2,cursor="hand2")

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

# TWO DIFFERENT EXIT BUTTON FUNCTIONS TO AVOID CONFLICTS WITH BINDINGS IN DIFFERENT SCREENS 
# (ESCAPE KEY BINDS TO DIFFERENT FUNCTIONS BASED ON SCREEN)

def bind_exit_menu(app):
    # Exit function to go back to main menu when Escape key is pressed
    def exit_to_menu(event=None):
        app.root.unbind("<Escape>")
        app.show_main_menu()

    app.root.bind("<Escape>", exit_to_menu)
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.bind("<Button-1>", lambda e: app.show_main_menu())

def bind_exit_home(app):
    # Exit function to go back to home screen (a.k.a first menu) when Escape key is pressed
    def exit_to_home(event=None):
        app.root.unbind("<Escape>")
        app.show_home()

    app.root.bind("<Escape>", exit_to_home)
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.bind("<Button-1>", lambda e: app.show_home())