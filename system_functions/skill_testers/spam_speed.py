import tkinter as tk
import time

def cps_counter(app):
    app.clear()

    clicks = 0
    start_time = None
    best_cps = 0
    current_cps = 0
    last_click_time = None  # Tracks the last time the user clicked
    update_cps_display()  # Start CPS decay process

    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))
    title_label = tk.Label(top_bar, text="Memory Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Button
    button = tk.Button(frame, text="Click Me!", font=("Arial", 16), width=15, height=2, command=update_count)
    button.grid(row=0, column=0, pady=10, padx=10)

    # Click count label
    click_label = tk.Label(frame, text="Total Clicks: 0", font=("Arial", 14))
    click_label.grid(row=1, column=0, pady=5)

    # CPS Label
    cps_label = tk.Label(frame, text="Clicks Per Second: 0.00", font=("Arial", 12))
    cps_label.grid(row=2, column=0, pady=5)

    # Best CPS Label
    best_cps_label = tk.Label(frame, text="Best CPS: 0.00", font=("Arial", 12))
    best_cps_label.grid(row=3, column=0, pady=5)

    # Reset Button
    reset_button = tk.Button(frame, text="Reset", font=("Arial", 12), command=reset_counter)
    reset_button.grid(row=4, column=0, pady=10)

    def update_count(self):
        nonlocal clicks, start_time, last_click_time, current_cps, best_cps
        clicks += 1
        current_time = time.time()

        if start_time is None:
            start_time = current_time  # Start time on first click

        last_click_time = current_time  # Update last click timestamp

        elapsed_time = current_time - start_time
        current_cps = clicks / elapsed_time if elapsed_time > 0 else 0

        # Update best CPS if current is higher
        if current_cps > best_cps:
            best_cps = current_cps

        # Update UI
        click_label.config(text=f"Total Clicks: {clicks}")
        cps_label.config(text=f"Clicks Per Second: {current_cps:.2f}")
        best_cps_label.config(text=f"Best CPS: {best_cps:.2f}")

    def update_cps_display(self):
        """Gradually decreases CPS if the player stops clicking."""
        nonlocal current_cps, last_click_time
        if last_click_time:
            time_since_last_click = time.time() - last_click_time

            # If the user hasn't clicked for 1 second, start decreasing CPS
            if time_since_last_click > 1:
                current_cps *= 0.9  # Reduce CPS by 10% every frame
                if current_cps < 0.1:  # If CPS gets really low, reset it to 0
                    current_cps = 0

        cps_label.config(text=f"Clicks Per Second: {current_cps:.2f}")

        # Call this function every 100ms to update the CPS display
        app.root.after(100, update_cps_display)

    def reset_counter(self):
        nonlocal clicks, start_time, best_cps, current_cps, last_click_time
        clicks = 0
        start_time = None
        best_cps = 0
        current_cps = 0
        last_click_time = None

        click_label.config(text="Total Clicks: 0")
        cps_label.config(text="Clicks Per Second: 0.00")
        best_cps_label.config(text="Best CPS: 0.00")
    
    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        from system_functions.skill_training_menu import show_skill_menu # Prevent circular import
        app.root.unbind("<Escape>")
        my_menu.destroy() # Clear menu so it doesn't leak into the next page
        frame.destroy()
        show_skill_menu(app)

    exit_btn = tk.Label(frame, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)