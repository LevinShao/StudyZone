import tkinter as tk

def show_memory_trainer(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    coming_soon = tk.Label(frame, text="Coming Soon!", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    coming_soon.pack(expand=True)

    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        # Import inside of function (to prevent circular import error)
        from system_functions.skill_training_menu import show_skill_menu

        app.root.unbind("<Escape>")
        show_skill_menu(app)

    exit_btn = tk.Label(frame, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)