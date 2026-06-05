import tkinter as tk
from system_functions.backend.ui_helpers import *

def show_public_blogs(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    coming_soon = tk.Label(frame, text="Coming Soon!", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    coming_soon.pack(expand=True)

    # EXIT BUTTON FUNCTIONS
    def exit_to_express_menu(event=None):
        from system_functions.inner_menus.express_yourself_menu import show_express_menu

        app.root.unbind("<Escape>")
        show_express_menu(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_express_menu)
    app.root.bind("<Escape>", exit_to_express_menu)