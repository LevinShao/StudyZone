import tkinter as tk
from db_files.data_manager import get_user_data, update_user_data

def show_goal_planner(app):
    app.clear()

    outer = tk.Frame(app.root, bg=app.BG_MAIN)
    outer.pack(expand=True)

    frame = tk.Frame(outer, bg=app.BG_CARD, padx=80, pady=40)
    frame.pack()

    tk.Label(frame, text="Goal Planner", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    user_data = get_user_data(app.current_user)
    goals = user_data["goals"]

    # INPUTS
    goal_entry, _ = app.create_field(frame, "Goal Title")
    deadline_entry, _ = app.create_field(frame, "Target Date (YYYY-MM-DD)")

    # PRIORITY TOGGLE
    priority_var = tk.BooleanVar()

    priority_checkbox = tk.Checkbutton(frame, text="Priority Goal", variable=priority_var, bg=app.BG_CARD, fg=app.TEXT, 
                                       selectcolor=app.BG_CARD, activebackground=app.BG_CARD, activeforeground=app.TEXT)
    priority_checkbox.pack(anchor="w", pady=10)

    # GOAL LIST
    listbox = tk.Listbox(frame, width=60, height=10)
    listbox.pack(pady=20)

    def refresh_list():
        listbox.delete(0, tk.END)
        for g in goals:
            priority_mark = "❗ " if g["priority"] else ""
            status = "✓" if g["done"] else "✗"
            listbox.insert(
                tk.END,
                f"{status} {priority_mark}{g['title']} ({g['date']})"
            )

    def add_goal():
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

    def complete_goal():
        selected = listbox.curselection()
        if selected:
            goals[selected[0]]["done"] = True
            update_user_data(app.current_user, user_data)
            refresh_list()

    def delete_goal():
        selected = listbox.curselection()
        if selected:
            goals.pop(selected[0])
            update_user_data(app.current_user, user_data)
            refresh_list()

    def exit_to_menu(event=None):
        app.root.unbind("<Escape>")
        app.show_main_menu()

    # BUTTONS
    tk.Button(frame, text="Add Goal", command=add_goal, bg=app.ACCENT, fg=app.TEXT).pack(pady=5)
    tk.Button(frame, text="Mark Complete", command=complete_goal, bg="#334155", fg=app.TEXT).pack(pady=5)
    tk.Button(frame, text="Delete Goal", command=delete_goal, bg="#334155", fg=app.TEXT).pack(pady=5)

    # EXIT BUTTON
    exit_btn = tk.Label(app.root, text="✖", fg="white", bg=app.ACCENT, font=("Segoe UI", 16),cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.bind("<Button-1>", lambda e: app.show_main_menu())
    app.root.bind("<Escape>", exit_to_menu)