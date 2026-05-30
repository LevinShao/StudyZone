import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from db_files.data_manager import get_user_data, update_user_data
from system_functions.backend.ui_helpers import create_small_button, bind_exit_menu

def show_task_tracker(app):
    app.clear()

    # OUTER FRAMES
    outer = tk.Frame(app.root, bg=app.BG_MAIN)
    outer.pack(expand=True, fill="both")

    frame = tk.Frame(outer, bg=app.BG_CARD, padx=100, pady=30)
    frame.pack(expand=True)

    tk.Label(frame, text="Task Tracker", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    # LOAD DATA
    user_data = get_user_data(app.current_user)
    tasks = user_data["tasks"]

    # INPUT FIELDS
    task_entry, _ = app.create_field(frame, "Task Name")
    desc_entry, _ = app.create_field(frame, "Description")
    deadline_entry, _ = app.create_field(frame, "Deadline (YYYY-MM-DD)")

    # Deadline error label
    error_deadline = tk.Label(frame, text="", fg="#ef4444", bg=app.BG_CARD)
    error_deadline.pack(anchor="w", pady=1)

    # Priority field
    tk.Label(frame, text="Priority", bg=app.BG_CARD, fg=app.TEXT).pack(anchor="w")

    priority_map = {
        "1 - Very Important": "1",
        "2 - Important": "2",
        "3 - Moderate": "3",
        "4 - Chill": "4",
        "5 - Casual": "5"
    }

    selected_priority = tk.StringVar()
    selected_priority.set("")

    priority_dropdown = ttk.Combobox(frame, textvariable=selected_priority, values=list(priority_map.keys()), state="readonly")
    priority_dropdown.pack(fill="x", pady=10)

    # Priority error label, right after priority dropdown
    error_priority = tk.Label(frame, text="", fg="#ef4444", bg=app.BG_CARD)
    error_priority.pack(anchor="w")

    # Listbox, will display tasks with their status and priority, double-click to view details in a popup
    listbox = tk.Listbox(frame, width=60, height=10)
    listbox.pack(pady=20, fill="both")

    # Refresh listbox with current tasks, showing status and priority
    def refresh_list():
        listbox.delete(0, tk.END)
        for t in tasks:
            status = "✓" if t["done"] else "✗"
            listbox.insert(tk.END, f"{status} {t['name']} (P{t['priority']})")

    def validate_inputs(event=None):
        # Input validation function to check deadline format and priority selection before enabling the Add Task button
        valid = True

        # Duplicate task check (NAME + DEADLINE)
        name = task_entry.get().strip().lower()
        deadline = deadline_entry.get().strip()

        for t in tasks:
            if t["name"].strip().lower() == name and t["deadline"] == deadline:
                error_deadline.config(text="This task already exists")
                add_btn.config(state="disabled")
                return

        # Deadline check
        deadline = deadline_entry.get().strip()
        if deadline == "":
            error_deadline.config(text="")
            valid = False
        elif deadline < datetime.now().strftime("%Y-%m-%d"):
            error_deadline.config(text="Deadline cannot be in the past")
            valid = False
        else:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                error_deadline.config(text="")
            except:
                error_deadline.config(text="Invalid date (YYYY-MM-DD)")
                valid = False

        # Priority check
        if selected_priority.get() not in priority_map:
            error_priority.config(text="Please select a priority")
            valid = False
        else:
            error_priority.config(text="")

        add_btn.config(state="normal" if valid else "disabled")

    def add_task(): # Add Task
        task = {
            "name": task_entry.get(),
            "desc": desc_entry.get(),
            "deadline": deadline_entry.get(),
            "priority": priority_map[selected_priority.get()],
            "done": False
        }

        if task["name"].strip() == "":
            return

        tasks.append(task)
        update_user_data(app.current_user, user_data)
        refresh_list()

        # Clear inputs
        task_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        selected_priority.set("")
        error_priority.config(text="")
        add_btn.config(state="disabled") # Used for re-disabling the add button after adding a task, re-enable after validating inputs again

    def edit_task(): # Edit Task
        selected = listbox.curselection()
        if not selected:
            return

        index = selected[0]
        task = tasks[index]

        # Popup Window
        edit_win = tk.Toplevel(app.root)
        edit_win.title("Edit Task")
        edit_win.configure(bg=app.BG_CARD)

        tk.Label(edit_win, text="Edit Task", font=("Segoe UI", 16, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

        # Input fields pre-filled with current task data
        name_entry = tk.Entry(edit_win, width=40)
        name_entry.insert(0, task["name"])
        name_entry.pack(pady=5)

        desc_entry = tk.Entry(edit_win, width=40)
        desc_entry.insert(0, task["desc"])
        desc_entry.pack(pady=5)

        deadline_entry_popup = tk.Entry(edit_win, width=40)
        deadline_entry_popup.insert(0, task["deadline"])
        deadline_entry_popup.pack(pady=5)

        priority_var = tk.StringVar()
        priority_options = list(priority_map.keys())

        # set current priority
        for key, val in priority_map.items():
            if val == task["priority"]:
                priority_var.set(key)

        priority_dropdown_popup = ttk.Combobox(edit_win, textvariable=priority_var, values=priority_options, state="readonly")
        priority_dropdown_popup.pack(pady=5)

        def save_changes(): 
            # Save changes to the task after editing
            task["name"] = name_entry.get()
            task["desc"] = desc_entry.get()
            task["deadline"] = deadline_entry_popup.get()
            task["priority"] = priority_map[priority_var.get()]

            update_user_data(app.current_user, user_data)
            refresh_list()
            edit_win.destroy()

        create_small_button(edit_win, "Save Changes", save_changes, app, primary=True).pack(pady=10)

    def complete_task(): 
        # Mark task as complete
        selected = listbox.curselection()
        if selected:
            tasks[selected[0]]["done"] = True
            update_user_data(app.current_user, user_data)
            refresh_list()

    def delete_task(): 
        # Delete task from list
        selected = listbox.curselection()
        if selected:
            tasks.pop(selected[0])
            update_user_data(app.current_user, user_data)
            refresh_list()

    def show_task_popup(task): 
        # Show task details in a popup
        details = (
            f"Name: {task['name']}\n\n"
            f"Description: {task['desc']}\n\n"
            f"Deadline: {task['deadline']}\n\n"
            f"Priority: P{task['priority']}\n\n"
            f"Status: {'Done' if task['done'] else 'Not Done'}"
        )
        messagebox.showinfo("Task Details", details)

    def view_task_details(event):
        # Get selected task and show details in a popup when double-clicking a task in the listbox
        selected = listbox.curselection()
        if selected:
            show_task_popup(tasks[selected[0]])

    listbox.bind("<Double-Button-1>", view_task_details)

    # Buttons
    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)

    # Row 1
    add_btn = create_small_button(btn_frame, "Add Task", add_task, app, primary=True)
    add_btn.grid(row=0, column=0, padx=15, pady=15)
    add_btn.config(state="disabled") # Initially disable the add button until valid inputs are provided
    create_small_button(btn_frame, "Edit Task", edit_task, app, primary=False).grid(row=0, column=1, padx=15, pady=15)

    # Row 2
    create_small_button(btn_frame, "Mark Complete", complete_task, app, primary=False).grid(row=1, column=0, padx=15, pady=10)
    create_small_button(btn_frame, "Delete Task", delete_task, app, primary=False).grid(row=1, column=1, padx=15, pady=10)

    # Exit Button
    bind_exit_menu(app)

    # Bindings
    deadline_entry.bind("<KeyRelease>", validate_inputs)
    priority_dropdown.bind("<<ComboboxSelected>>", validate_inputs)

    # Initial refresh to show existing tasks
    refresh_list()