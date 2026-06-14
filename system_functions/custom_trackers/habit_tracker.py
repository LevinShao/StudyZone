import tkinter as tk
from datetime import datetime
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data

def show_habit_tracker(app):
    app.clear()
    
    user_data = get_user_data(app.current_user)
    habits = user_data["habits"]
    today = datetime.now().strftime("%d %B %Y")

    # Main container
    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Habit Tracker", font=("Segoe UI", 28, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=30)

    # Top card for habit creation
    top_card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    top_card.pack(fill="x", padx=60)

    tk.Label(top_card, text="Habit Name", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    habit_entry = tk.Entry(top_card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    habit_entry.pack(fill="x", pady=(5, 15), ipady=5)

    # Major list box for habits
    listbox = tk.Listbox(container, font=("Segoe UI", 11), bg="#111827", fg="white", height=28)
    listbox.pack(fill="x", padx=60, pady=30)

    selected_index = [-1] # Use a list to allow modification inside nested functions, -1 means no selection

    # Refresh the listbox with current habits
    def refresh_list():
        listbox.delete(0, tk.END)

        for habit in habits:
            # Check if the habit is completed today
            completed_today = today in habit["completed_dates"]
            status = "✅" if completed_today else "❌"
            total = len(habit["completed_dates"])
            listbox.insert(tk.END, f"{status} | {habit['name']} | Total Completions: {total}")

        update_complete_button()

    # Update complete button
    def update_complete_button():
        if selected_index[0] == -1:
            complete_btn.config(state="disabled")
            return

        habit = habits[selected_index[0]]

        if today in habit["completed_dates"]:
            complete_btn.config(state="disabled")
        else:
            complete_btn.config(state="normal")

    # Select habit from list box
    def select_habit(event=None):
        selected = listbox.curselection()

        if not selected:
            # No selection, disable complete button and return
            return

        selected_index[0] = selected[0] # Update the selected index
        update_complete_button()

    listbox.bind("<<ListboxSelect>>", select_habit) # Bind selection event to update the selected index and button state

    # Create a new habit
    def create_habit():
        name = habit_entry.get().strip()

        if name == "":
            return

        # Prevent duplicate habit names (case-insensitive)
        for habit in habits:
            if habit["name"].lower() == name.lower():
                return

        habits.append({
            "name": name,
            "created_date": today,
            "completed_dates": []
        })

        update_user_data(app.current_user, user_data)
        habit_entry.delete(0, tk.END)
        refresh_list()

    # Complete a habit
    def complete_habit():
        if selected_index[0] == -1: # No selection, disable complete button and return
            return

        habit = habits[selected_index[0]]

        if today not in habit["completed_dates"]:
            habit["completed_dates"].append(today)

        update_user_data(app.current_user, user_data)
        refresh_list()
        update_complete_button()

    # Delete a habit
    def delete_habit():
        if selected_index[0] == -1:
            return

        habits.pop(selected_index[0]) # Remove the selected habit from the list
        selected_index[0] = -1 # Reset selection after deletion, -1 means no selection
        update_user_data(app.current_user, user_data)
        refresh_list()
        update_complete_button()

    # Buttons
    btn_frame = tk.Frame(container, bg=BG_MAIN)
    btn_frame.pack(pady=10)

    create_small_button(btn_frame, "Create Habit", create_habit, app, primary=True).grid(row=0, column=0, padx=15)
    complete_btn = create_small_button(btn_frame, "Complete Today", complete_habit, app, primary=True)
    complete_btn.grid(row=0, column=1, padx=15)
    complete_btn.config(state="disabled") # Initially disable the complete button until a habit is selected
    create_small_button(btn_frame, "Delete Habit", delete_habit, app, primary=False).grid(row=0, column=2, padx=15)

    # EXIT BUTTON FUNCTIONS
    def exit_to_trackers_menu(event=None):
        from system_functions.inner_menus.custom_trackers import show_trackers_menu

        app.root.unbind("<Escape>")
        show_trackers_menu(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_trackers_menu)
    app.root.bind("<Escape>", exit_to_trackers_menu)

    refresh_list()
    update_complete_button()