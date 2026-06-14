import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data

def sticky_main(app):
    app.clear()

    # LOAD DATA
    user_data = get_user_data(app.current_user)
    sticky_notes = user_data["sticky_notes"]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Sticky Notes", font=("Segoe UI", 28, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=30)

    # Main Card
    card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    card.pack(fill="both", expand=True, padx=60, pady=(0, 20))

    # Current Date is automatically added to each entry and cannot be edited by the user
    current_date = datetime.now().strftime("%d %B %Y")
    tk.Label(card, text=f"Date: {current_date}", font=("Segoe UI", 12, "bold"), bg=BG_CARD, fg="#94a3b8").pack(anchor="w", pady=(0, 20))

    # Main Content
    tk.Label(card, text="Write Down Your Thoughts...", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    note_text = tk.Text(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white", wrap="word", height=4)
    note_text.pack(fill="x", pady=(5, 30))

    # List box containing previous sticky notes
    tk.Label(card, text="Previous Sticky Notes", font=("Segoe UI", 16), bg=BG_CARD, fg=TEXT).pack(pady=(5, 5))
    listbox = tk.Listbox(card, font=("Segoe UI", 11), bg="#111827", fg="white", width=120, height=15)
    listbox.pack(fill="both", expand=True, padx=10, pady=20)

    selected_index = [-1] # -1 indicates no selection, using list for mutability in nested functions

    # Refresh Notes
    def refresh_notes():
        listbox.delete(0, tk.END)

        for note in sticky_notes:
            # Create a preview of the note content for display in the list box
            preview = note["content"]

            # Shorten preview if too long
            if len(preview) > 80:
                preview = preview[:80] + "..."

            listbox.insert(tk.END, f"{note['date']} | {preview}")

    # Load Note
    def load_note(event=None):
        selected = listbox.curselection() # Get the currently selected index in the list box

        if not selected:
            return

        # Update the selected index to the current selection
        index = selected[0]
        selected_index[0] = index

    listbox.bind("<<ListboxSelect>>", load_note)

    # View Note
    def view_note(event=None):
        selected = listbox.curselection()

        if not selected:
            return

        index = selected[0]
        note = sticky_notes[index]

        details = (
            f"Date: {note['date']}\n\n"
            f"Content:\n\n{note['content']}"
        )

        messagebox.showinfo("Sticky Note", details)

    listbox.bind("<Double-Button-1>", view_note)

    # New Note
    def new_note():
        selected_index[0] = -1 # Reset selected index to indicate no selection when creating a new note
        note_text.delete("1.0", tk.END) # Clear the text box for new note entry

    # Save Note
    def save_note():
        content = note_text.get("1.0", tk.END).strip() # Get the content from the text box and remove leading/trailing whitespace

        if content == "":
            return

        sticky_notes.append({"content": content, "date": current_date}) # Add the new note to the list of sticky notes

        # Update user data
        update_user_data(app.current_user, user_data)
        note_text.delete("1.0", tk.END)
        refresh_notes()

    # Edit Note
    def edit_note():
        selected = listbox.curselection()

        if not selected:
            return

        index = selected[0]
        note = sticky_notes[index]

        # Popup Window and Editing Interface
        edit_win = tk.Toplevel(app.root)
        edit_win.title("Edit Sticky Note")
        edit_win.configure(bg=BG_CARD)

        tk.Label(edit_win, text="Edit Sticky Note", font=("Segoe UI", 16, "bold"), bg=BG_CARD, fg=TEXT).pack(pady=15)
        tk.Label(edit_win, text=f"Date: {note['date']}", font=("Segoe UI", 11), bg=BG_CARD, fg="#94a3b8").pack(pady=(0, 10))

        edit_text = tk.Text(edit_win, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white", wrap="word", width=50, height=10)
        edit_text.pack(padx=20, pady=10)
        edit_text.insert("1.0", note["content"])

        def save_changes():
            # Update the note content with the edited text, then save to user data and refresh the list of notes
            note["content"] = edit_text.get("1.0", tk.END).strip()
            update_user_data(app.current_user, user_data)
            refresh_notes()
            edit_win.destroy()

        create_small_button(edit_win, "Save Changes", save_changes, app, primary=True).pack(pady=15)

    # Delete Note
    def delete_note():
        selected = listbox.curselection()

        if not selected:
            return

        # Remove the selected note from the list of sticky notes, update user data, and refresh the list box
        sticky_notes.pop(selected[0])
        update_user_data(app.current_user, user_data)
        selected_index[0] = -1
        note_text.delete("1.0", tk.END)
        refresh_notes()

    # Buttons
    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.pack(pady=10)

    create_small_button(btn_frame, "Save Note", save_note, app, primary=True).grid(row=0, column=0, padx=15)
    create_small_button(btn_frame, "New Note", new_note, app, primary=True).grid(row=0, column=1, padx=15)
    create_small_button(btn_frame, "Edit Note", edit_note, app, primary=False).grid(row=0, column=2, padx=15)
    create_small_button(btn_frame, "Delete Note", delete_note, app, primary=False).grid(row=0, column=3, padx=15)

    # Exit Button
    def exit_to_express_menu(event=None):
        from system_functions.inner_menus.express_yourself_menu import show_express_menu

        app.root.unbind("<Escape>")
        show_express_menu(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_express_menu)
    app.root.bind("<Escape>", exit_to_express_menu)

    refresh_notes()