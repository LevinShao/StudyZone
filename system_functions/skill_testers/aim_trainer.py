import tkinter as tk
import random
from db_files.data_manager import get_user_data, update_user_data

GAME_DURATION = 30 # Set 30 second timer for each game

def show_aim_trainer(app):
    app.clear()

    # Load User Data
    user_data = get_user_data(app.current_user)
    aim_data = user_data["aim_trainer"]

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title and Stats
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="Aim Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Initial Game Stats
    score = 0
    hits = 0
    clicks = 0
    time_left = GAME_DURATION

    # Left Side + Empty Space for Centering Title
    left_spacer = tk.Frame(top_bar, bg=app.BG_CARD, width=80)
    left_spacer.pack(side="left")

    # Right Side (Labels)
    right_spacer = tk.Frame(top_bar, bg=app.BG_CARD)
    right_spacer.pack(side="right", padx=25)

    timer_label = tk.Label(right_spacer, text=f"Time: {GAME_DURATION}", font=("Segoe UI", 14, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    timer_label.pack(anchor="e")

    score_label = tk.Label(right_spacer, text="Score: 0", font=("Segoe UI", 14, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    score_label.pack(anchor="e")

    highscore_label = tk.Label(right_spacer, text=f"Personal Best: {aim_data['high_score']}", font=("Segoe UI", 14, "bold"), bg=app.BG_CARD, fg="#22c55e")
    highscore_label.pack(anchor="e")

    # Main Canvas Area
    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Game State Variables
    targets = []
    running = True
    spawn_job = None
    timer_job = None

    app.root.update_idletasks()

    def get_canvas_size():
        # Get the current size of the canvas, accounting for cases where it might not be fully rendered yet
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 100:
            width = app.root.winfo_screenwidth()

        if height < 100:
            height = app.root.winfo_screenheight()

        return width, height

    def create_target():
        # Get canvas size each time to ensure targets spawn within bounds even if window is resized
        canvas_width, canvas_height = get_canvas_size()
        radius = 30

        x = random.randint(radius, canvas_width - radius)
        y = random.randint(radius, canvas_height - radius)

        target = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="red")
        return target

    def update_score():
        score_label.config(text=f"Score: {score}")

    def on_click(event):
        # Increment total clicks for accuracy calculation (nonlocal means we can modify the variable defined in the outer function)
        nonlocal score, hits, clicks

        clicks += 1
        # Get all items under the click (in case of multiple targets overlapping, which is rare but possible, still trying to find a proper fix)
        items = canvas.find_overlapping(event.x, event.y, event.x, event.y)

        hit = False # Flag to check if we hit a target, used to prevent multiple hits from one click if targets overlap

        for item in items:
            # Check if the clicked item is in our targets list
            if item in targets:
                canvas.delete(item)
                targets.remove(item)

                score += 1
                hits += 1

                update_score()
                hit = True
                break

    canvas.bind("<Button-1>", on_click)

    def spawn_targets():
        # Use nonlocal to modify the spawn_job variable defined in the outer function
        # this allows us to cancel it later when the game ends
        nonlocal spawn_job

        if not running:
            return

        if len(targets) < 5:
            targets.append(create_target())

        # Spawn a new target every 700 ms but only if there are less than 5 targets on the screen (prevent overcrowding)
        spawn_job = app.root.after(700, spawn_targets)

    def countdown():
        # Use nonlocal to modify the timer_job variable defined in the outer function
        nonlocal time_left, running, timer_job

        if not running:
            return

        # Decrement the timer and update the label (if time runs out, end the game)
        time_left -= 1
        timer_label.config(text=f"Time: {time_left}")

        if time_left <= 0:
            end_game()
            return

        timer_job = app.root.after(1000, countdown) # Update timer every second

    def end_game():
        # When the game ends, stop spawning targets and stop the timer, then show the summary screen
        nonlocal running

        running = False

        try:
            # Cancel any scheduled target spawns or timer updates to prevent them from running after the game has ended
            if spawn_job:
                app.root.after_cancel(spawn_job)

            if timer_job:
                app.root.after_cancel(timer_job)
        except:
            pass

        accuracy = 0 # Calculate accuracy but prevent division by zero if the player never clicked

        if clicks > 0:
            accuracy = round((hits / clicks) * 100)

        # Save Statistics to User Data
        if score > aim_data["high_score"]:
            aim_data["high_score"] = score

        if accuracy > aim_data["best_accuracy"]:
            aim_data["best_accuracy"] = accuracy

        aim_data["games_played"] += 1
        update_user_data(app.current_user, user_data)

        # Summary Screen
        canvas.destroy()

        summary = tk.Frame(frame, bg=app.BG_CARD)
        summary.pack(expand=True)

        tk.Label(summary, text="Game Over", font=("Segoe UI", 30, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)
        tk.Label(summary, text=f"Final Score: {score}", font=("Segoe UI", 18), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)
        tk.Label(summary, text=f"Accuracy: {accuracy}%", font=("Segoe UI", 18), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)
        tk.Label(summary, text=f"Personal Best: {aim_data['high_score']}", font=("Segoe UI", 18), bg=app.BG_CARD, fg="#22c55e").pack(pady=10)

        restart_btn = tk.Button(summary, text="Play Again", command=lambda: show_aim_trainer(app), bg=app.ACCENT, fg="white", font=("Segoe UI", 14, "bold"))
        restart_btn.pack(pady=20)

    # Exit Button + Function
    def exit_to_skill_menu(event=None):
        # Import inside of function (to prevent circular import error)
        from system_functions.inner_menus.skill_training_menu import show_skill_menu

        nonlocal running
        running = False

        try:
            if spawn_job:
                app.root.after_cancel(spawn_job)

            if timer_job:
                app.root.after_cancel(timer_job)
        except:
            pass

        app.root.unbind("<Escape>")
        show_skill_menu(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)

    # Game Initialization
    spawn_targets()
    countdown()