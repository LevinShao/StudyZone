import tkinter as tk
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data
from system_functions.express_yourself.journal.open_entry import open_journal_entry

def show_entries(app):
    app.clear()

    user_data = get_user_data(app.current_user)
    journal_entries = user_data["journal_entries"]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Previous Journal Entries", font=("Segoe UI", 24, "bold"), bg=BG_MAIN, fg=TEXT).pack(pady=30)

    listbox = tk.Listbox(container, font=("Segoe UI", 11), bg="#111827", fg="white", width=120, height=25)
    listbox.pack(padx=30, pady=20)

    # Refresh the listbox with the latest journal entries
    def refresh():
        listbox.delete(0, tk.END)

        for entry in journal_entries:
            # Show the date, title, weather, and emotion for each entry in a preview format
            preview = f"{entry['date']} | {entry['title']} | {entry['weather']} | {entry['emotion']}"
            listbox.insert(tk.END, preview)

    # Open the selected journal entry when double-clicked
    def open_selected_entry(event=None):
        selected = listbox.curselection()

        if not selected:
            return

        open_journal_entry(app, selected[0])

    listbox.bind("<Double-Button-1>", open_selected_entry)

    # Exit Button
    def exit_to_create_menu(event=None):
        from system_functions.express_yourself.journal.create_new_entry import create_new_journal

        app.root.unbind("<Escape>")
        create_new_journal(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_create_menu)
    app.root.bind("<Escape>", exit_to_create_menu)

    refresh()