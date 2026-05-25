import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from db_files.data_manager import get_user_data, update_user_data
from system_functions.backend.ui_helpers import create_small_button, create_field, bind_exit_menu

def show_goal_planner(app):
    app.clear()

    # OUTER FRAMES
    outer = tk.Frame(app.root, bg=app.BG_MAIN)
    outer.pack(expand=True)

    frame = tk.Frame(outer, bg=app.BG_CARD, padx=80, pady=40)
    frame.pack()

    tk.Label(frame, text="Goal Planner", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    user_data = get_user_data(app.current_user)
    goals = user_data["goals"]

    # INPUTS
    goal_entry, _ = create_field(frame, "Goal Title")
    deadline_entry, _ = create_field(frame, "Target Date (YYYY-MM-DD)")

    error_duplicate_name = tk.Label(frame, text="", fg="#ef4444", bg=app.BG_CARD)
    error_duplicate_name.pack(anchor="w", pady=1)

    error_deadline = tk.Label(frame, text="", fg="#ef4444", bg=app.BG_CARD)
    error_deadline.pack(anchor="w", pady=1)

    # PRIORITY TOGGLE
    priority_var = tk.BooleanVar()
    priority_checkbox = tk.Checkbutton(frame, text="Priority Goal", variable=priority_var, bg=app.BG_CARD, fg=app.TEXT, 
                                       selectcolor=app.BG_CARD, activebackground=app.BG_CARD, activeforeground=app.TEXT)
    priority_checkbox.pack(anchor="w", pady=10)

    # GOAL LIST
    listbox = tk.Listbox(frame, width=60, height=10)
    listbox.pack(pady=20)

    def refresh_list():
        # Refresh the list box with current goals
        listbox.delete(0, tk.END)
        for g in goals:
            priority_mark = "❗ " if g["priority"] else ""
            status = "✓" if g["done"] else "✗"
            listbox.insert(tk.END, f"{status} {priority_mark}{g['title']} ({g['date']})")

    def validate_inputs(event=None):
        # Input validation function to check date format and priority selection before enabling the Add Goal button
        valid = True

        # Goal title check
        if goal_entry.get().strip() == "":
            error_duplicate_name.config(text="Goal name required")
            add_btn.config(state="disabled")
            return
        
        # Duplicate goal check (same title, case-insensitive)
        title = goal_entry.get().strip().lower()

        for g in goals:
            if g["title"].strip().lower() == title:
                error_duplicate_name.config(text="Goal with this name already exists")
                add_btn.config(state="disabled")
                return

        error_duplicate_name.config(text="")

        # Deadline check
        date = deadline_entry.get().strip()
        if date == "":
            error_deadline.config(text="")
            valid = False
        elif date < datetime.now().strftime("%Y-%m-%d"):
            error_deadline.config(text="Deadline cannot be in the past")
            valid = False
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                error_deadline.config(text="")
            except:
                error_deadline.config(text="Invalid date (YYYY-MM-DD)")
                valid = False

        add_btn.config(state="normal" if valid else "disabled")

    def add_goal():
        # Add a new goal to the list after validating inputs, then save to user data and refresh the list box

        goal = {
            "title": goal_entry.get(),
            "date": deadline_entry.get(),
            "priority": priority_var.get(),
            "done": False
        }

        if goal["title"].strip() == "":
            return

        goals.append(goal)
        update_user_data(app.current_user, user_data)
        refresh_list()

        # Clear inputs
        goal_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        priority_var.set(False)
        error_duplicate_name.config(text="")
        error_deadline.config(text="")
        add_btn.config(state="disabled")

    def edit_goal():
        # Edit Goal
        selected = listbox.curselection()
        if not selected:
            return

        index = selected[0]
        goal = goals[index]

        # Popup Window
        edit_win = tk.Toplevel(app.root)
        edit_win.title("Edit Goal")
        edit_win.configure(bg=app.BG_CARD)

        tk.Label(edit_win, text="Edit Goal", font=("Segoe UI", 16, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

        name_entry = tk.Entry(edit_win, width=40)
        name_entry.insert(0, goal["title"])
        name_entry.pack(pady=5)

        deadline_entry_popup = tk.Entry(edit_win, width=40)
        deadline_entry_popup.insert(0, goal["date"])
        deadline_entry_popup.pack(pady=5)
        
        priority_var_popup = tk.BooleanVar(value=goal["priority"])
        priority_checkbox_popup = tk.Checkbutton(edit_win, text="Priority Goal", variable=priority_var_popup, bg=app.BG_CARD, fg=app.TEXT,
                                               selectcolor=app.BG_CARD, activebackground=app.BG_CARD, activeforeground=app.TEXT)
        priority_checkbox_popup.pack(anchor="w", pady=10)

        def save_changes(): 
            # Save Changes
            goal["title"] = name_entry.get()
            goal["date"] = deadline_entry_popup.get()
            goal["priority"] = priority_var_popup.get()

            update_user_data(app.current_user, user_data)
            refresh_list()
            edit_win.destroy()

        create_small_button(edit_win, "Save Changes", save_changes, app, primary=True).pack(pady=10)

    def complete_goal():
        # Mark goal as complete
        selected = listbox.curselection()
        if selected:
            goals[selected[0]]["done"] = True
            update_user_data(app.current_user, user_data)
            refresh_list()

    def delete_goal():
        # Delete selected goal from the list
        selected = listbox.curselection()
        if selected:
            goals.pop(selected[0])
            update_user_data(app.current_user, user_data)
            refresh_list()

    def show_goal_popup(goal): 
        # Show goal details in a popup
        details = (
            f"Name: {goal['title']}\n\n"
            f"Deadline: {goal['date']}\n\n"
            f"Priority: {goal['priority']}\n\n"
            f"Status: {'Done' if goal['done'] else 'Not Done'}"
        )
        messagebox.showinfo("Goal Details", details)

    def view_goal_details(event):
        # Get selected goal and show details in a popup when double-clicking a goal in the listbox
        selected = listbox.curselection()
        if selected:
            show_goal_popup(goals[selected[0]])

    listbox.bind("<Double-Button-1>", view_goal_details)

    # Buttons
    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)

    # Row 1
    add_btn = create_small_button(btn_frame, "Add Goal", add_goal, app, primary=True)
    add_btn.grid(row=0, column=0, padx=15, pady=15)
    create_small_button(btn_frame, "Edit Goal", edit_goal, app, primary=False).grid(row=0, column=1, padx=15, pady=15)

    # Row 2
    create_small_button(btn_frame, "Mark Complete", complete_goal, app, primary=False).grid(row=1, column=0, padx=15, pady=10)
    create_small_button(btn_frame, "Delete Goal", delete_goal, app, primary=False).grid(row=1, column=1, padx=15, pady=10)

    # Exit button
    bind_exit_menu(app)

    # Bindings
    goal_entry.bind("<KeyRelease>", validate_inputs)
    deadline_entry.bind("<KeyRelease>", validate_inputs)

    # Initial refresh to show existing goals
    refresh_list()