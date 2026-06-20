import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db_files.data_manager import get_user_data, update_user_data
from system_functions.backend.ui_helpers import create_small_button
from system_functions.squares.calendar.calendar_view import show_calendar

def show_day_view(app, year, month, day):
    # Show the day view with events for that specific day
    app.clear()

    user_data = get_user_data(app.current_user)
    events = user_data["events"]

    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=40, pady=40)
    frame.pack(expand=True)

    date_str = f"{year}-{month:02d}-{day:02d}"
    today = datetime.now().strftime("%Y-%m-%d")
    is_past = date_str < today

    tk.Label(frame, text=f"Events for {date_str}", font=("Segoe UI", 20), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    title_entry, _ = app.create_field(frame, "Event Title")
    time_entry, _ = app.create_field(frame, "Time (HH:MM)")

    listbox = tk.Listbox(frame, width=50)
    listbox.pack(pady=20)

    def get_day_events():
        # Retrieve events for the specified date by filtering the user's events based on the date string
        return [e for e in events if e["date"] == date_str]

    def refresh_list():
        listbox.delete(0, tk.END)
        for e in get_day_events():
            status = "✓" if e.get("done") else "✗"
            listbox.insert(tk.END, f"{status} {e['time']} - {e['title']}")

    def add_event():
        # Add a new event to the user's events list with validation for time format and past date restriction
        if is_past:
            return

        try:
            # Validate time format before adding the event
            datetime.strptime(time_entry.get(), "%H:%M")
        except:
            # If the format is incorrect, an exception will be raised and we can simply return without adding the event
            return

        event = {
            "title": title_entry.get(),
            "date": date_str,
            "time": time_entry.get(),
            "datetime": f"{date_str} {time_entry.get()}",
            "done": False,
            "notified": False
        }

        events.append(event)
        update_user_data(app.current_user, user_data)
        refresh_list()

    def get_selected_event():
        # Get the currently selected event in the listbox by matching the selected index with the filtered list of events for that day
        selected = listbox.curselection()
        if not selected:
            return None
        return get_day_events()[selected[0]]

    def edit_event():
        # Allow users to edit the title and time of the selected event
        if is_past:
            return

        event = get_selected_event()
        if not event:
            return

        # Open a popup window to edit the selected event's title and time with validation for time format
        win = tk.Toplevel(app.root)
        win.configure(bg=app.BG_CARD)

        title_entry = tk.Entry(win, width=40)
        title_entry.insert(0, event["title"])
        title_entry.pack(pady=5)

        time_entry = tk.Entry(win, width=40)
        time_entry.insert(0, event["time"])
        time_entry.pack(pady=5)

        def save():
            try:
                datetime.strptime(time_entry.get(), "%H:%M")
            except:
                return

            # Update the event with the new title and time then save to user data and refresh the list box in the day view
            event["title"] = title_entry.get()
            event["time"] = time_entry.get()
            event["datetime"] = f"{event['date']} {time_entry.get()}"

            update_user_data(app.current_user, user_data)
            refresh_list()
            win.destroy()

        tk.Button(win, text="Save", command=save, bg=app.ACCENT, fg=app.TEXT).pack(pady=10)

    def complete_event():
        # Mark the selected event as complete, then update user data and refresh the list box
        event = get_selected_event()
        if event:
            event["done"] = True
            update_user_data(app.current_user, user_data)
            refresh_list()

    def delete_event():
        # Delete the selected event from the list of events, then update user data and refresh the list box
        event = get_selected_event()
        if event:
            events.remove(event)
            update_user_data(app.current_user, user_data)
            refresh_list()

    def show_event_popup(event): 
        # Show event details in a popup
        details = (
            f"Title: {event['title']}\n\n"
            f"Date: {event['date']}\n\n"
            f"Time: {event['time']}\n\n"
            f"Status: {'Done' if event['done'] else 'Not Done'}"
        )
        messagebox.showinfo("Event Details", details)

    def view_event_details(event):
        # Get selected event and show details in a popup when double-clicking an event in the list box
        selected = listbox.curselection()
        if selected:
            show_event_popup(events[selected[0]])

    # Back Arrow + Exit to Calendar on Escape Key
    def exit_to_calendar(event=None):
        app.root.unbind("<Escape>")
        show_calendar(app, year, month)

    app.root.bind("<Escape>", exit_to_calendar) # Bind Escape key to exit back to calendar view from day view
    listbox.bind("<Double-Button-1>", view_event_details) # Bind double-click to view event details

    exit_btn = tk.Label(app.root, text="←", fg="white", bg="#ef4444", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)    
    
    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_calendar)

    # Button Frame
    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)
    
    # Buttons
    add_btn = create_small_button(btn_frame, "Add Event", add_event, app, primary=True)
    add_btn.grid(row=0, column=0, padx=10, pady=10)
    edit_btn = create_small_button(btn_frame, "Edit Event", edit_event, app, primary=False)
    edit_btn.grid(row=0, column=1, padx=10, pady=10)
    create_small_button(btn_frame, "Mark Complete", complete_event, app, primary=False).grid(row=1, column=0, padx=10, pady=10)
    create_small_button(btn_frame, "Delete Event", delete_event, app, primary=False).grid(row=1, column=1, padx=10, pady=10)

    if is_past:
        # Disable add/edit buttons for past days since it doesn't make sense to add or edit events for a day that has already passed. 
        # Users can still mark events as complete or delete them if they want.
        add_btn.config(state="disabled")
        edit_btn.config(state="disabled")

    refresh_list()