import tkinter as tk
from tkinter import ttk
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data
from system_functions.squares.study_tools.notebook.open_page import open_notebook_page

def show_notebook_pages(app):
    app.clear()

    # Fetch user data
    user_data = get_user_data(app.current_user)
    notebook = user_data["notebook"]
    filter = ["All", "Mathematics", "English", "Physics", "Chemistry", "Biology", "Economics", "Engineering", "Software", "Study Tips", "Personal", "Other"]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Your Notebook Pages", font=("Segoe UI", 24, "bold"), bg=BG_MAIN, fg=TEXT).pack(pady=30)
    tk.Label(container, text=f"{len(notebook)} Pages", font=("Segoe UI", 11), bg=BG_MAIN, fg="#94a3b8").pack()

    # Category Filter
    filter_frame = tk.Frame(container, bg=BG_MAIN)
    filter_frame.pack()

    tk.Label(filter_frame, text="Category:", font=("Segoe UI", 11), bg=BG_MAIN, fg=TEXT).pack(side="left", padx=(0,10))
    filter_var = tk.StringVar(value="All") # Set default filter to All
    filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_var, values=filter, state="readonly") # Create a read only dropdown
    filter_dropdown.pack(side="left")
    filter_dropdown.current(filter.index("All")) # Set default filter to All

    listbox = tk.Listbox(container, font=("Segoe UI", 11), bg="#111827", fg="white", width=120, height=25)
    listbox.pack(padx=30, pady=20)

    # Note: There were many bugs encountered during development here. Some of them required solutions beyond my technical ability.
    # Google AI Overview Responses were utilized in a purely instructional manner to fix these bugs.

    # Refresh the listbox with the latest pages.
    # We use *args here for compatibility with trace_add callback
    def refresh(*args):
        listbox.delete(0, tk.END)
        selected_category = filter_var.get() # Get the selected category from the dropdown

        for entry in notebook:
            # Where a category is not specified, we classify it as Other
            category = entry.get("category", "Other")

            if selected_category != "All" and category != selected_category:
                # Skip pages that do not match the selected category
                continue

            # Show the date, title, and category for each entry in a preview format.
            # If the date is empty, shown Unknown instead. If the title is empty, show "Untitled" instead.
            preview = (f"{entry.get('date_created','Unknown')} | {entry.get('title','Untitled')} | {category}")
            listbox.insert(tk.END, preview)

    # Open the selected page when double-clicked
    def open_selected_entry(event=None):
        selected = listbox.curselection() # Get the index of the selected item

        if not selected:
            return

        selected_category = filter_var.get() # Get the selected category from the dropdown
        filtered_entries = [] # We will use a filtered list to store the pages that match the selected category

        for entry in notebook:
            if selected_category == "All" or entry.get("category", "Other") == selected_category:
                # If the selected category is All, or the page category matches the selected category, add the page to the filtered list
                filtered_entries.append(entry)

        chosen = filtered_entries[selected[0]] # Get the selected page from the filtered list
        actual_index = notebook.index(chosen) # Get the actual index of the selected page in the notebook list. We need this because the filtered list is a subset of the notebook list.
        open_notebook_page(app, actual_index) # Open the selected page.

    listbox.bind("<Double-Button-1>", open_selected_entry)

    # EXIT BUTTON FUNCTIONS
    def exit_btn():
        from system_functions.squares.study_tools.notebook.create_new_page import create_new_page
        bind_exit_inner_menu(app, create_new_page)

    exit_btn()

    # Whenever the selected filter category changes, refresh the listbox. 
    # We use *args since Tkinter auto-passes three arguments to callback. To ignore them, *args is the best way.
    filter_var.trace_add("write", lambda *args: refresh())
    refresh() # Initial refresh to adjust listbox