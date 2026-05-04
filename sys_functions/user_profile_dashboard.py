import tkinter as tk
from tkinter import messagebox
import json
from db_files.data_manager import load_data, save_data

def show_profile_menu(self):
    self.clear() # Clear the current screen to show the profile menu

    frame = tk.Frame(self.root, bg=self.BG_CARD, padx=100, pady=100)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Logged in as: {self.current_user}", font=("Segoe UI", 18), bg=self.BG_CARD, fg=self.TEXT).pack(pady=20)

    def logout(): 
        # Logout function with confirmation dialog
        if not messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out of your account?"):
            return
        
        self.current_user = None
        self.show_home()

    def delete_account():
        # Delete account function with confirmation dialog
        if not messagebox.askyesno("Delete Account Confirmation", "Are you sure you want to delete your account?\nThis action cannot be undone."):
            return
        
        ACCOUNTDB_FILE = "db_files/users.json"

        # delete from users.json
        with open(ACCOUNTDB_FILE, "r") as f:
            users = json.load(f)

        if self.current_user in users:
            del users[self.current_user]

        with open(ACCOUNTDB_FILE, "w") as f:
            json.dump(users, f, indent=4)

        # also delete from data.json
        data = load_data()
        if self.current_user in data:
            del data[self.current_user]
            save_data(data)

        # logout and show first menu (home screen)
        self.current_user = None
        self.show_home()

    # Buttons
    tk.Button(frame, text="← Back", command=self.show_main_menu, bg=self.BG_CARD, fg=self.TEXT, width=20, height=2).pack(pady=10)
    tk.Button(frame, text="Log Out", command=logout, bg=self.ACCENT, fg=self.TEXT, width=20, height=2).pack(pady=10)
    tk.Button(frame, text="Delete Account", command=delete_account, bg=self.ACCENT, fg=self.TEXT, width=20, height=2).pack(pady=10)