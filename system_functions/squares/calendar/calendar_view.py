import tkinter as tk
import time
from datetime import datetime
import calendar                    # For calendar generation
import threading                   # For running the reminder loop in the background
from plyer import notification     # Notification system
from db_files.data_manager import get_user_data, update_user_data
from system_functions.backend.ui_helpers import bind_exit_menu

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

    def prev_year():
        m = month
        y = year - 1
        show_calendar(app, y, m)

    def next_year():
        m = month
        y = year + 1
        show_calendar(app, y, m)

    # Header with month and year display and navigation buttons
    tk.Button(header, text="◀◀", command=prev_year, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10)    
    tk.Button(header, text="◀", command=prev_month, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10)
    tk.Label(header, text=f"{calendar.month_name[month]} {year}", font=("Segoe UI", 16, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(side="left", padx=20)
    tk.Button(header, text="▶", command=next_month, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10)
    tk.Button(header, text="▶▶", command=next_year, bg=app.ACCENT, fg=app.TEXT).pack(side="left", padx=10) 

    # Calendar Grid
    cal = calendar.monthcalendar(year, month)

    grid = tk.Frame(frame, bg=app.BG_CARD)
    grid.pack()

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days):
        tk.Label(grid, text=d, bg=app.BG_CARD, fg=app.TEXT).grid(row=0, column=i)

    def open_day(day):
        from system_functions.squares.calendar.calendar_events import show_day_view
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
    if not hasattr(app, "reminder_started"): # use hasattr to check if the attribute has been set
        threading.Thread(target=reminder_loop, args=(app, app.current_user), daemon=True).start() # Start the reminder loop in a background thread
        app.reminder_started = True # Set the attribute to True to prevent multiple loops

    bind_exit_menu(app)