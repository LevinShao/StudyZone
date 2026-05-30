import tkinter as tk
from tkinter import messagebox
import json
from db_files.data_manager import load_data, save_data
from system_functions.backend.ui_helpers import bind_exit_menu
import pygame # Import pygame to stop music playback when logging out or deleting account

def show_profile_menu(app):
    app.clear() # Clear the current screen to show the profile menu

    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=100, pady=100)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Logged in as: {app.current_user}", font=("Segoe UI", 18), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)

    def logout(): 
        # Logout function with confirmation dialog
        if not messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out of your account?"):
            return
        
        app.current_user = None
        pygame.mixer.music.stop()
        app.show_home()

    def delete_account():
        # Delete account function with confirmation dialog
        if not messagebox.askyesno("Delete Account Confirmation", "Are you sure you want to delete your account?\nThis action cannot be undone."):
            return
        
        ACCOUNTDB_FILE = "db_files/users.json"

        # delete from users.json
        with open(ACCOUNTDB_FILE, "r") as f:
            users = json.load(f)

        if app.current_user in users:
            del users[app.current_user]

        with open(ACCOUNTDB_FILE, "w") as f:
            json.dump(users, f, indent=4)

        # also delete from data.json
        data = load_data()
        if app.current_user in data:
            del data[app.current_user]
            save_data(data)

        # logout and show first menu (home screen)
        app.current_user = None
        pygame.mixer.music.stop()
        app.show_home()

    # Buttons
    tk.Button(frame, text="← Back", command=app.show_main_menu, bg=app.BG_CARD, fg=app.TEXT, width=20, height=2).pack(pady=10)
    tk.Button(frame, text="Log Out", command=logout, bg=app.ACCENT, fg=app.TEXT, width=20, height=2).pack(pady=10)
    tk.Button(frame, text="Delete Account", command=delete_account, bg=app.ACCENT, fg=app.TEXT, width=20, height=2).pack(pady=10)

    # EXIT BUTTON
    bind_exit_menu(app)