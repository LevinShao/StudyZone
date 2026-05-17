import tkinter as tk
import time
import random
from db_files.data_manager import get_user_data, update_user_data

def show_reaction_trainer(app):
    app.clear()

    # Load User Data
    user_data = get_user_data(app.current_user)
    reaction_data = user_data["reaction_trainer"]

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title and Stats
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="Reaction Time Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Left Side
    left_spacer = tk.Frame(top_bar, bg=app.BG_CARD, width=80)
    left_spacer.pack(side="left")

    # Right Side (Stats)
    right_spacer = tk.Frame(top_bar, bg=app.BG_CARD)
    right_spacer.pack(side="right", padx=30)

    # Personal Best
    best_time = reaction_data.get("best_time", 0)

    if best_time == 0:
        best_display = "-- ms"
    else:
        best_display = f"{best_time} ms"

    pb_label = tk.Label(right_spacer, text=f"Best: {best_display}", font=("Segoe UI", 14, "bold"), bg=app.BG_CARD, fg="#4ade80")
    pb_label.pack(anchor="e")

    # Attempt Counter
    attempts = 0

    attempt_label = tk.Label(right_spacer, text="Attempt 0", font=("Segoe UI", 12), bg=app.BG_CARD, fg=app.TEXT)
    attempt_label.pack(anchor="e")

    # Main Canvas
    canvas = tk.Canvas(frame, bg="red", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Texts
    main_text = canvas.create_text(0, 0, text="Click to Start", fill="white", font=("Segoe UI", 42, "bold"))
    sub_text = canvas.create_text(0, 0, text="Welcome to the Reaction Time Trainer!", fill="white", font=("Segoe UI", 18))

    # Dynamically center text
    def center_text(event=None):
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        canvas.coords(main_text, width / 2, height / 2)
        canvas.coords(sub_text, width / 2, (height / 2) - 80)

    # Bind the canvas resize event to the center_text function to keep text centered when window size changes
    canvas.bind("<Configure>", center_text)

    # Main Game State Variables
    start_time = None
    game_started = False
    can_click = False
    after_id = None

    # Major Click Handler
    def on_canvas_click(event):
        nonlocal game_started, can_click, start_time, after_id

        # Start new round
        if not game_started:
            start_game()
            return

        # Clicked too early
        if game_started and not can_click:
            if after_id:
                # Cancel the scheduled turn_green call since the user clicked early
                frame.after_cancel(after_id)

            canvas.config(bg="red")
            canvas.itemconfig(main_text, text="Too Early!")
            canvas.itemconfig(sub_text, text="Click to try again")

            game_started = False
            return

        # Correct click
        if can_click:
            reaction_time = int((time.time() - start_time) * 1000) # Convert to ms and round to int for cleaner display

            canvas.config(bg="red")
            canvas.itemconfig(main_text, text=f"{reaction_time} ms")
            canvas.itemconfig(sub_text, text="Click to play again")

            # Save the Best Reaction Time (if it's a new personal best)
            current_best = reaction_data.get("best_time", 0)

            if current_best == 0 or reaction_time < current_best:
                # Update user data with new best time and refresh the personal best label
                reaction_data["best_time"] = reaction_time
                update_user_data(app.current_user, user_data)
                pb_label.config(text=f"Best: {reaction_time} ms")

            game_started = False
            can_click = False

    # Make both left click and spacebar trigger the same function for better accessibility
    canvas.bind("<Button-1>", on_canvas_click)
    canvas.bind("<Key-space>", on_canvas_click)
    canvas.focus_set() # Required to ensure the canvas can receive keyboard events (like spacebar presses)

    # Start Game Function (initializes a new round, sets random delay for green state)
    def start_game():
        # Use nonlocal to modify variables defined in the outer scope of this function
        nonlocal game_started, can_click, after_id, attempts

        # Increment attempt counter and update label per new round
        attempts += 1
        attempt_label.config(text=f"Attempt {attempts}")

        # Set initial state for new round
        game_started = True
        can_click = False

        canvas.config(bg="red")
        canvas.itemconfig(main_text, text="Wait for Green")
        canvas.itemconfig(sub_text, text="● ● ●")

        delay = random.uniform(2, 7) # 2-7 seconds random delay before turning green, used random_uniform because it allows decimal seconds 
        after_id = frame.after(int(delay * 1000), turn_green) # Schedule turn_green to run after the random delay, *1000 to convert s to ms for after() method

    # Green State Function (called after random delay, allows user to click and records reaction time)
    def turn_green():
        nonlocal start_time, can_click

        canvas.config(bg="#4ade80")
        canvas.itemconfig(main_text, text="CLICK!")
        canvas.itemconfig(sub_text, text="!!!")

        start_time = time.time() # Record the time when the screen turns green
        can_click = True

    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        # Import inside of function (to prevent circular import error)
        from system_functions.skill_training_menu import show_skill_menu

        app.root.unbind("<Escape>")
        show_skill_menu(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)