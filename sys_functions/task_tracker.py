import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from db_files.data_manager import get_user_data, update_user_data

def show_task_tracker(app):
    app.clear()

    def create_small_button(parent, text, command, app, primary=True):
        # Helper function to create small buttons with hover effect.
        # Used in the task tracker for actions like edit, complete, delete. 
        # Will appear in goal planner too
        bg = app.ACCENT if primary else "#22C55E"
        btn = tk.Label(parent, text=text, bg=bg, fg="white", font=("Segoe UI", 12, "bold"), width=18, height=2, cursor="hand2")

        def on_enter(e):
            btn.config(bg="#dc2626" if primary else "#16a34a")

        def on_leave(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e: command())

        return btn

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
    error_deadline.pack(anchor="w", pady=(2, 10))

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

        tasks.append(task)
        update_user_data(app.current_user, user_data)
        refresh_list()

        # Clear inputs
        task_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        selected_priority.set("")
        error_priority.config(text="")
        add_btn.config(state="disabled")

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

        def save_changes(): # Save Changes
            task["name"] = name_entry.get()
            task["desc"] = desc_entry.get()
            task["deadline"] = deadline_entry_popup.get()
            task["priority"] = priority_map[priority_var.get()]

            update_user_data(app.current_user, user_data)
            refresh_list()
            edit_win.destroy()

        create_small_button(edit_win, "Save Changes", save_changes, app, primary=True).pack(pady=10)

    def complete_task(): # Mark Task as Complete
        selected = listbox.curselection()
        if selected:
            tasks[selected[0]]["done"] = True
            update_user_data(app.current_user, user_data)
            refresh_list()

    def delete_task(): # Delete Task
        selected = listbox.curselection()
        if selected:
            tasks.pop(selected[0])
            update_user_data(app.current_user, user_data)
            refresh_list()

    def show_task_popup(task): # Show Task Details in a Popup
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
    create_small_button(btn_frame, "Edit Task", edit_task, app, primary=False).grid(row=0, column=1, padx=15, pady=15)

    # Row 2
    create_small_button(btn_frame, "Mark Complete", complete_task, app, primary=False).grid(row=1, column=0, padx=15, pady=10)
    create_small_button(btn_frame, "Delete Task", delete_task, app, primary=False).grid(row=1, column=1, padx=15, pady=10)
    
    # Exit button (top left corner)
    def exit_to_menu(event=None):
        app.root.unbind("<Escape>")
        app.show_main_menu()

    app.root.bind("<Escape>", exit_to_menu) # Exit to main menu on Escape key press

    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16),cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.bind("<Button-1>", lambda e: app.show_main_menu())

    # Bindings
    deadline_entry.bind("<KeyRelease>", validate_inputs)
    priority_dropdown.bind("<<ComboboxSelected>>", validate_inputs)

    # Initial refresh to show existing tasks
    refresh_list()