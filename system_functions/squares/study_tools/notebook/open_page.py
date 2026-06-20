import tkinter as tk
from tkinter import ttk
from datetime import datetime
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data

def open_notebook_page(app, index):
    app.clear()

    # Fetch user data
    user_data = get_user_data(app.current_user)
    notebook = user_data["notebook"]
    categories = ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Economics", "Engineering", "Software", "Study Tips", "Personal", "Other"]
    entry = notebook[index]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    # Main Card
    card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    card.pack(fill="both", expand=True, padx=50, pady=40)

    # Main Title
    tk.Label(card, text="Title", font=("Segoe UI", 11), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    title_edit = tk.Entry(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    title_edit.pack(fill="x", pady=(5, 15), ipady=5)
    title_edit.insert(0, entry["title"]) # Insert the title of the journal entry into the title edit field

    tk.Label(card, text="Category", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    category_var = tk.StringVar(value=entry.get("category", "Other")) # Set the default category to Other
    category_dropdown = ttk.Combobox(card, textvariable=category_var, values=categories, state="readonly", font=("Segoe UI", 12))
    category_dropdown.pack(fill="x", pady=(5, 15))

    # Select the current category
    if category_var.get() in categories:
        category_dropdown.current(categories.index(category_var.get())) # Select the current category in the dropdown
    else:
        category_dropdown.current(categories.index("Other")) # If the category is not in the dropdown, select Other

    # DATE
    tk.Label(card, text=f"Created: {entry.get('date_created','Unknown')}", font=("Segoe UI", 11, "bold"), bg=BG_CARD, fg="#94a3b8").pack(anchor="w")
    tk.Label(card, text=f"Last Modified: {entry.get('last_modified', entry.get('date_created','Unknown'))}", font=("Segoe UI", 11), bg=BG_CARD, fg="#94a3b8").pack(anchor="w", pady=(0,20))

    # MAIN CONTENTS
    text_box = tk.Text(card, font=("Segoe UI", 12), bg="#111827", fg="white", wrap="word", insertbackground="white")
    text_box.pack(fill="both", expand=True)
    text_box.insert("1.0", entry["content"])

    # We must start in read-only mode, and we need a mutable variable to track whether we're in edit mode or not for the toggle_edit function
    editing = [False]

    def set_read_only():
        # Set all widgets to read-only mode, all buttons are disabled
        edit_btn.config(state="disabled")
        title_edit.config(state="disabled")
        text_box.config(state="disabled")
        category_dropdown.config(state="disabled")

    def set_editable():
        # Set all widgets to editable mode, all buttons are enabled
        # We won't config edit button here, we'll do that in toggle_edit
        title_edit.config(state="normal")
        text_box.config(state="normal")
        category_dropdown.config(state="normal")

    # Edit / Save Changes
    def toggle_edit():
        # Enter Edit Mode
        if not editing[0]:
            editing[0] = True
            set_editable()
            edit_btn.config(text="Save Changes")

        # Save Changes and Exit Edit Mode
        else:
            entry["title"] = title_edit.get().strip()
            entry["content"] = text_box.get("1.0", tk.END).strip()
            entry["category"] = category_var.get()
            entry["last_modified"] = datetime.now().strftime("%d %B %Y")

            update_user_data(app.current_user, user_data)
            editing[0] = False
            set_read_only()
            edit_btn.config(text="Edit Entry")

    # Delete Entry
    def delete_entry():
        from system_functions.squares.study_tools.notebook.view_your_pages import show_notebook_pages

        notebook.pop(index)
        update_user_data(app.current_user, user_data)
        show_notebook_pages(app)

    # Buttons
    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.pack(pady=20)

    edit_btn = create_small_button(btn_frame, "Edit Entry", toggle_edit, app, primary=True)
    edit_btn.grid(row=0, column=0, padx=10)
    create_small_button(btn_frame, "Delete Entry", delete_entry, app, primary=False).grid(row=0, column=1, padx=10)

    # EXIT BUTTON FUNCTIONS
    def exit_to_entries(event=None):
        from system_functions.squares.study_tools.notebook.view_your_pages import show_notebook_pages

        app.root.unbind("<Escape>")
        show_notebook_pages(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_entries)
    app.root.bind("<Escape>", exit_to_entries)

    set_read_only() # Set read only initially to disable all widgets and re-enable when editing is enabled