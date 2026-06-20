import tkinter as tk
from system_functions.backend.ui_helpers import bind_exit_menu

# THE FOLLOWING CODE IS ORIGINALLY FORKED FROM PROXLIGHT'S POMODORO TIMER TUTORIAL FOR CUSTOMTKINTER
# I MODIFIED IT SLIGHTLY SO THAT IT FITS WITH NORMAL TKINTER AND HAS SOME ADDITIONAL FEATURES, AND I ALSO STYLED IT IN A WAY I LIKED BETTER
# SHOUTOUT TO PROXLIGHT FOR THE INSPIRATION OF THIS CODE!
# LINK TO ORIGINAL: https://github.com/Proxlight/Pomodoro-Timer

def show_pomodoro_timer(app):
    app.clear()

    # ------------------ Variables ------------------
    FOCUS_TIME = 1500 # 25 mins lock in time
    SHORT_BREAK = 300 # 5 mins short break
    LONG_BREAK = 900 # 15 mins long break then end of the cycle

    time_left = FOCUS_TIME # Track time left in the current session, starts at focus time and counts down

    running = False # Timer running state, set to False so that it is initially paused at 25 mins
    timer_id = None # Track the timer after() ID to prevent multiple loops

    session_type = "focus" # track session type, can be focus, short_break, or long_break. starts as focus
    completed_sessions = 0 # count completed focus sessions to determine when to take long break

    # ------------------ UI ------------------
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Focus label
    focus_label = tk.Label(frame, text="🧠 Focus Timer", fg="#4A1C1C", bg="#FADBD6", padx=20, pady=6, font=("Helvetica", 14, "normal"))
    focus_label.pack(pady=30)

    # Timer
    timer_label = tk.Label(frame, text="25:00", font=("Helvetica", 96, "bold"), fg="#3B0D0D", bg=app.BG_CARD, justify="center")
    timer_label.pack(expand=True)

    # Controls
    controls = tk.Frame(frame, bg=app.BG_CARD)
    controls.pack(pady=40)

    # ------------------ Functions ------------------
    def update_timer():
        nonlocal time_left, running, timer_id, session_type, completed_sessions

        if not running:
            return

        minutes = time_left // 60
        seconds = time_left % 60

        timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        # TIMER STILL RUNNING
        if time_left > 0:
            time_left -= 1
            timer_id = app.root.after(1000, update_timer)

        # TIMER FINISHED
        else:

            # FOCUS SESSION FINISHED
            if session_type == "focus":
                completed_sessions += 1

                # LONG BREAK EVERY 4 SESSIONS, USE MODULUS TO CHECK IF COMPLETED SESSIONS IS DIVISIBLE BY 4
                if completed_sessions % 4 == 0:
                    session_type = "long_break"
                    time_left = LONG_BREAK
                    focus_label.configure(text="🎮 Long Break", bg="#dbeafe", fg="#1e3a8a")

                else:
                    session_type = "short_break"
                    time_left = SHORT_BREAK
                    focus_label.configure(text="☕ Short Break", bg="#d1fae5", fg="#065f46")

                # Continue automatically
                timer_id = app.root.after(1000, update_timer)

            # BREAK FINISHED
            else:

                # End session after long break
                if session_type == "long_break":
                    running = False

                    play_btn.configure(text="▶")
                    focus_label.configure(text="✅ Pomodoro Complete", bg="#fde68a", fg="#92400e")
                    timer_label.configure(text="Done!")

                    return

                # Return to focus mode after short break
                session_type = "focus"
                time_left = FOCUS_TIME
                focus_label.configure(text="🧠 Focus Timer", bg="#FADBD6", fg="#4A1C1C")

                # Continue automatically
                timer_id = app.root.after(1000, update_timer)

    def start_pause():
        nonlocal running, timer_id

        running = not running # Toggle running state
        
        # Update play button text and start/pause timer accordingly
        if running:
            play_btn.configure(text="⏸")
            update_timer()
        else:
            play_btn.configure(text="▶")
            if timer_id:
                app.root.after_cancel(timer_id)

    def reset_timer():
        nonlocal time_left, running, timer_id, session_type, completed_sessions

        running = False

        if timer_id:
            # Cancel any existing timer loop to prevent multiple loops running simultaneously
            app.root.after_cancel(timer_id)

        # Reset all variables to initial state
        session_type = "focus"
        completed_sessions = 0
        time_left = FOCUS_TIME
        minutes = time_left // 60
        seconds = time_left % 60

        focus_label.configure(text="🧠 Focus Timer", bg="#FADBD6", fg="#4A1C1C")
        play_btn.configure(text="▶")
        timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    def adjust_time(amount): 
        # This function currently doesn't work as expected, the basic functionality is there but there is currently no way to actually adjust the time
        # Will figure out later if possible
        nonlocal time_left, running

        if not running:
            # Only allow time adjustment when timer is paused to prevent complications with the timer loop and variable states
            time_left += amount

            if time_left < 0:
                time_left = 0

            minutes = time_left // 60
            seconds = time_left % 60
            timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    # ------------------ Buttons ------------------
    menu_btn = tk.Button(controls, text="⋯", width=6, height=3, bg="#FADBD6", fg="#3B0D0D", font=("Helvetica", 22, "bold"), command=lambda: adjust_time(-60))
    menu_btn.grid(row=0, column=0, padx=20)

    play_btn = tk.Button(controls, text="▶", width=15, height=3, bg="#FF7A73", fg="white", font=("Helvetica", 26, "bold"), command=start_pause)
    play_btn.grid(row=0, column=1, padx=20)

    reset_btn = tk.Button(controls, text="⏭", width=6, height=3, bg="#FADBD6", fg="#3B0D0D", font=("Helvetica", 22, "bold"), command=reset_timer)
    reset_btn.grid(row=0, column=2, padx=20)

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