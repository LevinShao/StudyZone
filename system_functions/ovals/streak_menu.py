import tkinter as tk
import json
from system_functions.backend.ui_helpers import *

def show_streak_menu(app):
    app.clear()

    with open("db_files/users.json", "r") as f:
        users = json.load(f)

    user = users.get(app.current_user)

    if not user:
        return

    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=50, pady=50)
    frame.pack(expand=True)

    tk.Label(frame, text="🔥 Login Streak", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)
    tk.Label(frame, text=f"{user['streak']} Days", font=("Segoe UI", 42, "bold"), bg=app.BG_CARD, fg="#f97316").pack()
    tk.Label(frame, text=f"Best Streak: {user.get('best_streak', 0)} Days", font=("Segoe UI", 14), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)
    tk.Label(frame, text=f"Last Login:\n{user.get('last_login_date', 'N/A')}", font=("Segoe UI", 12), bg=app.BG_CARD, fg=app.SUBTLE).pack(pady=10)

    bind_exit_menu(app)