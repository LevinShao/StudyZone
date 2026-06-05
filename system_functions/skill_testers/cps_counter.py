import tkinter as tk
import time

# This entire code is ripped off from one of my older projects, made back in year 8
# I have since then cleaned it up and added some new features, but the core logic and structure is the same as the original code

def show_cps_counter(app):
    app.clear()

    # Major State Variables
    clicks = 0
    start_time = None
    best_cps = 0
    current_cps = 0
    last_click_time = None
    cps_after_id = None

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="CPS Counter", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Main Content Area
    content = tk.Frame(frame, bg=app.BG_CARD)
    content.pack(expand=True)

    # Main Labels
    click_label = tk.Label(content, text="Total Clicks: 0", font=("Arial", 14), bg=app.BG_CARD, fg=app.TEXT)
    click_label.pack(pady=5)

    cps_label = tk.Label(content, text="Clicks Per Second: 0.00", font=("Arial", 12), bg=app.BG_CARD, fg=app.TEXT)
    cps_label.pack(pady=5)

    best_cps_label = tk.Label(content, text="Best CPS: 0.00", font=("Arial", 12), bg=app.BG_CARD, fg=app.TEXT)
    best_cps_label.pack(pady=5)

    # Function to update click count and CPS
    def update_count():
        nonlocal clicks, start_time, last_click_time, current_cps, best_cps

        clicks += 1
        current_time = time.time()

        if start_time is None:
            start_time = current_time

        last_click_time = current_time
        elapsed_time = current_time - start_time
        current_cps = clicks / elapsed_time if elapsed_time > 0 else 0

        if current_cps > best_cps:
            best_cps = current_cps

        click_label.config(text=f"Total Clicks: {clicks}")
        cps_label.config(text=f"Clicks Per Second: {current_cps:.2f}")
        best_cps_label.config(text=f"Best CPS: {best_cps:.2f}")

    # Function to continuously update CPS display and handle decay
    def update_cps_display():
        nonlocal current_cps, last_click_time, cps_after_id

        if last_click_time:
            time_since_last_click = time.time() - last_click_time

            # If the user hasn't clicked for 1 second, start decreasing CPS
            if time_since_last_click > 1:
                current_cps *= 0.90 # Decay CPS by 10% every second of inactivity

                if current_cps < 0.1:
                    current_cps = 0

        cps_label.config(text=f"Clicks Per Second: {current_cps:.2f}")
        cps_after_id = app.root.after(100, update_cps_display)

    def reset_counter():
        nonlocal clicks, start_time, best_cps, current_cps, last_click_time

        # Reset all state variables to initial values
        clicks = 0
        start_time = None
        best_cps = 0
        current_cps = 0
        last_click_time = None

        click_label.config(text="Total Clicks: 0")
        cps_label.config(text="Clicks Per Second: 0.00")
        best_cps_label.config(text="Best CPS: 0.00")

    # Buttons
    button = tk.Button(content, text="Click Me!", font=("Arial", 16), width=15, height=2, command=update_count)
    button.pack(pady=10)

    reset_button = tk.Button(content, text="Reset", font=("Arial", 12), command=reset_counter)
    reset_button.pack(pady=10)

    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        nonlocal cps_after_id
        from system_functions.inner_menus.skill_training_menu import show_skill_menu
        app.root.unbind("<Escape>")

        if cps_after_id:
            app.root.after_cancel(cps_after_id)

        frame.destroy()
        show_skill_menu(app)

    exit_btn = tk.Label(frame, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)

    # Start CPS decay process
    update_cps_display()