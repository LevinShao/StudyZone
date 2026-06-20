import tkinter as tk
from tkinter import ttk
from datetime import datetime
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data
from system_functions.squares.study_tools.notebook.view_your_pages import show_notebook_pages

def create_new_page(app):
    app.clear()

    # Fetch user data
    user_data = get_user_data(app.current_user)
    notebook = user_data["notebook"]
    categories = ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Economics", "Engineering", "Software", "Study Tips", "Personal", "Other"]

    container, canvas = create_scrollable_page(app.root, BG_MAIN)

    tk.Label(container, text="Digital Notebook", font=("Segoe UI", 28, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=30)

    # Main Card
    card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    card.pack(fill="both", expand=True, padx=60, pady=(0, 20))

    # Current Date is automatically added to each entry and cannot be edited by the user
    current_date = datetime.now().strftime("%d %B %Y")
    tk.Label(card, text=f"Date: {current_date}", font=("Segoe UI", 12, "bold"), bg=BG_CARD, fg="#94a3b8").pack(anchor="w", pady=(0, 20))

    # Title and Info Inputs
    tk.Label(card, text="Title", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    title_entry = tk.Entry(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    title_entry.pack(fill="x", pady=(5, 15), ipady=6)

    # Category Dropdown
    tk.Label(card, text="Category", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    category_var = tk.StringVar(value="Other") # Set default category to Other, stringvar means the dropdown will update this variable when the user selects a category
    category_dropdown = ttk.Combobox(card, textvariable=category_var, values=categories, state="readonly") # Create a read only dropdown
    category_dropdown.pack(fill="x", pady=(5, 20))
    category_dropdown.current(categories.index("Other")) # Set default category to Other for the actual dropdown

    # Main Contents
    tk.Label(card, text="Notebook Page", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    content_text = tk.Text(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white", wrap="word", height=23)
    content_text.pack(fill="x", pady=(5, 30))

    # Clear all input fields
    def clear_fields():
        # Used for the new entry button
        title_entry.delete(0, tk.END) # Clear title entry from start to beginning
        content_text.delete("1.0", tk.END) # use 1.0 to delete from the start of the text box to the end
        category_var.set("Other") # Set default category to Other for the dropdown on field reset

    def save_entry():
        # Get all the data from the fields and save it as a new journal entry in the user's data, then clear the fields for a new entry
        title = title_entry.get().strip()
        content = content_text.get("1.0", tk.END).strip()

        if title == "" and content == "": 
            # at minimum, there should be a title or some content to save an entry
            return

        # Append the new entry to the user's journal entries and update the user data
        notebook.append({
            "title": title if title else "Untitled Note",
            "category": category_var.get(),
            "content": content,
            "date_created": current_date,
            "last_modified": current_date
        })

        update_user_data(app.current_user, user_data)
        clear_fields() # Clear fields after saving the entry

    # Buttons
    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.pack()

    create_small_button(btn_frame, "Save Entry", save_entry, app, primary=True).grid(row=0, column=0, padx=15)
    create_small_button(btn_frame, "New Entry", clear_fields, app, primary=True).grid(row=0, column=1, padx=15)
    create_small_button(btn_frame, "View Previous Entries", lambda: show_notebook_pages(app), app, primary=False).grid(row=0, column=2, padx=15)

    # EXIT BUTTON FUNCTIONS
    def exit_to_studymenu(event=None):
        from system_functions.squares.inner_menus.study_tools import show_studymenu

        app.root.unbind("<Escape>")
        show_studymenu(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_studymenu)
    app.root.bind("<Escape>", exit_to_studymenu)