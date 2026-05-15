import tkinter as tk
import time
import random

def show_reaction_trainer(app):
    app.clear()

    start_time = None
    timer_running = False

    # Inspired by Human Benchmark
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title and Stats
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    left_spacer = tk.Frame(top_bar, bg=app.BG_CARD, width=80)
    left_spacer.pack(side="left")

    # Center Title
    title_label = tk.Label(top_bar, text="Reaction Time Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Main Canvas Area
    canvas = tk.Canvas(frame, bg="red", highlightthickness=0)
    canvas.pack(pady = 20, fill="both", expand=True)

    label = tk.Label(frame, text="Click to Start. Wait for Green!", font=("Arial", 14))
    label.pack(pady=20)

    # Results Label
    result_label = tk.Label(frame, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    def on_canvas_click(event):
        if not timer_running:
            # Game starts/waits
            start_game()
        else:
            # Measure reaction time
            reaction_time = int((time.time() - start_time) * 1000)
            canvas.config(bg="red")
            result_label.config(text=f"Reaction Time: {reaction_time} ms")
            timer_running = False
            label.config(text="Click to play again!")

    canvas.bind("<Button-1>", on_canvas_click)

    def start_game():
        nonlocal timer_running

        timer_running = True
        label.config(text="Wait for Green...")
        result_label.config(text="")
        canvas.config(bg="red")
        
        # Random delay between 2 and 5 seconds
        delay = random.uniform(2, 5)
        
        # Schedule green color change
        frame.after(int(delay * 1000), make_green)

    def make_green():
        nonlocal start_time

        if timer_running:
            canvas.config(bg="green")
            start_time = time.time()
            label.config(text="CLICK NOW!")