import tkinter as tk
from system_functions.backend.ui_helpers import bind_exit_menu 

def show_pomodoro_timer(app):
    app.clear()

    # ------------------ Variables ------------------
    WORK_TIME = 25 * 60
    time_left = WORK_TIME
    running = False
    timer_id = None # Track the timer after() ID to prevent multiple loops

    # ------------------ UI ------------------
    # Focus label
    focus_label = tk.Label(app, text="🧠 Focus", fg="#4A1C1C", bg="#FADBD6", padx=20, pady=6, font=("Helvetica", 14, "normal"))
    focus_label.pack(pady=30)

    # Timer
    timer_label = tk.Label(app, text="25\n00", font=("Helvetica", 96, "bold"), fg="#3B0D0D", bg=app.BG_CARD, justify="center")
    timer_label.pack(expand=True)

    # Controls
    controls = tk.Frame(app, bg=app.BG_CARD)
    controls.pack(pady=40)

    # ------------------ Functions ------------------
    def update_timer():
        nonlocal time_left, running, timer_id
        
        if running and time_left >= 0:
            minutes = time_left // 60
            seconds = time_left % 60
            timer_label.configure(text=f"{minutes:02d}\n{seconds:02d}")
            time_left -= 1
            timer_id = app.after(1000, update_timer)
        elif time_left < 0:
            timer_label.configure(text="Time's\nUp!")
            running = False
            play_btn.configure(text="▶")

    def start_pause():
        nonlocal running, timer_id
        running = not running
        
        if running:
            play_btn.configure(text="⏸")
            update_timer()
        else:
            play_btn.configure(text="▶")
            if timer_id:
                app.after_cancel(timer_id) # Stop the scheduled after loop

    def reset_timer():
        nonlocal time_left, running, timer_id
        running = False
        time_left = WORK_TIME
        if timer_id:
            app.after_cancel(timer_id)
        play_btn.configure(text="▶")
        timer_label.configure(text="25\n00")

    menu_btn = tk.Button(controls, text="⋯", width=6, height=3, bg="#FADBD6", fg="#3B0D0D", font=("Helvetica", 22, "bold"))
    menu_btn.grid(row=0, column=0, padx=10)

    play_btn = tk.Button(controls, text="▶", width=8, height=3, bg="#FF7A73", fg="white", font=("Helvetica", 26, "bold"), command=start_pause)
    play_btn.grid(row=0, column=1, padx=10)

    reset_btn = tk.Button(controls, text="⏭", width=6, height=3, bg="#FADBD6", fg="#3B0D0D", font=("Helvetica", 22, "bold"), command=reset_timer)
    reset_btn.grid(row=0, column=2, padx=10)

    bind_exit_menu(app)