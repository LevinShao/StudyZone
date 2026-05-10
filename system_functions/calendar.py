import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import calendar                    # For calendar generation
import threading                   # For running the reminder loop in the background
from plyer import notification     # Notification system
from db_files.data_manager import get_user_data, update_user_data
from system_functions.backend.ui_helpers import create_small_button, bind_exit_menu

def send_notification(title, message):
    # Send a desktop notification using Plyer
    notification.notify(title=title, message=message, timeout=5)

def reminder_loop(app, username):
    # This function runs in a separate "thread" and checks every 30 seconds for any events that are due for notification
    # A thread is an independent flow of execution so it allows the app to remain responsive while this loop runs in the background
    while True:
        user_data = get_user_data(username)
        events = user_data["events"]

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        for event in events:
            # Check if the event is due for notification and hasn't been notified yet
            if not event.get("notified") and event["datetime"] == now:
                send_notification("StudyZone Reminder", event["title"])
                event["notified"] = True

        update_user_data(username, user_data)
        time.sleep(30)

def show_calendar(app, year=None, month=None):
    # Show the calendar view with the ability to add/edit/delete events for each day
    # also a reminder system that notifies users of upcoming events at their scheduled time.
    # The calendar also visually distinguishes past days and allows users to navigate between months.
    app.clear()

    user_data = get_user_data(app.current_user)
    events = user_data["events"]

    if year is None or month is None:
        # Default to the current month and year if not provided
        now = datetime.now()
        year = now.year
        month = now.month

    today = datetime.now().strftime("%Y-%m-%d")

    outer = tk.Frame(app.root, bg=app.BG_MAIN)
    outer.pack(expand=True)

    frame = tk.Frame(outer, bg=app.BG_CARD, padx=40, pady=30)
    frame.pack()

    tk.Label(frame, text="Calendar & Reminders", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    # Months Navigation Header
    header = tk.Frame(frame, bg=app.BG_CARD)
    header.pack(pady=10)

    def prev_month():
        m = month - 1
        y = year
        if m < 1:
            m = 12
            y -= 1
        show_calendar(app, y, m)

    def next_month():
        m = month + 1
        y = year
        if m > 12:
            m = 1
            y += 1
        show_calendar(app, y, m)

    # Header with month and year display and navigation buttons
    tk.Button(header, text="◀", command=prev_month, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10)
    tk.Label(header, text=f"{calendar.month_name[month]} {year}", font=("Segoe UI", 16, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(side="left", padx=20)
    tk.Button(header, text="▶", command=next_month, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10)

    # Calendar Grid
    cal = calendar.monthcalendar(year, month)

    grid = tk.Frame(frame, bg=app.BG_CARD)
    grid.pack()

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days):
        tk.Label(grid, text=d, bg=app.BG_CARD, fg=app.TEXT).grid(row=0, column=i)

    def open_day(day):
        if day == 0:
            return
        show_day_view(app, year, month, day)

    for r, week in enumerate(cal):
        # Loop through each day in the week and create a button for it. 
        # If the day is 0, it means it's an empty cell in the calendar (days from previous/next month) so we just create an empty label.
        for c, day in enumerate(week):
            if day == 0:
                tk.Label(grid, text="", bg=app.BG_CARD).grid(row=r+1, column=c)
                continue

            date_str = f"{year}-{month:02d}-{day:02d}"

            if date_str < today:
                # Past days are greyed out, current and future days are a different shade of grey
                bg_color = "#363A46"
            else:
                bg_color = "#4B5563"

            tk.Button(grid, text=str(day), width=5, height=2, bg=bg_color, fg="white", command=lambda d=day: open_day(d)).grid(row=r+1, column=c, padx=3, pady=3)

    # Start reminder loop once
    if not hasattr(app, "reminder_started"):
        threading.Thread(target=reminder_loop, args=(app, app.current_user), daemon=True).start()
        app.reminder_started = True

    bind_exit_menu(app)

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

    def refresh():
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
        refresh()

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

        t = tk.Entry(win, width=40)
        t.insert(0, event["title"])
        t.pack(pady=5)

        ti = tk.Entry(win, width=40)
        ti.insert(0, event["time"])
        ti.pack(pady=5)

        def save():
            try:
                datetime.strptime(ti.get(), "%H:%M")
            except:
                return

            # Update the event with the new title and time then save to user data and refresh the list box in the day view
            event["title"] = t.get()
            event["time"] = ti.get()
            event["datetime"] = f"{event['date']} {ti.get()}"

            update_user_data(app.current_user, user_data)
            refresh()
            win.destroy()

        tk.Button(win, text="Save", command=save, bg=app.ACCENT, fg=app.TEXT).pack(pady=10)

    def complete_event():
        # Mark the selected event as complete, then update user data and refresh the list box
        event = get_selected_event()
        if event:
            event["done"] = True
            update_user_data(app.current_user, user_data)
            refresh()

    def delete_event():
        # Delete the selected event from the list of events, then update user data and refresh the list box
        event = get_selected_event()
        if event:
            events.remove(event)
            update_user_data(app.current_user, user_data)
            refresh()

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

    refresh()