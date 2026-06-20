import tkinter as tk
import random
import time

# CREDITS TO YOUTUBE TUTORIAL Code With Don

def show_typing_app(app):
    app.clear()

    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title and Stats
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="Typing Speed Test", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # LOAD SENTENCES
    try:
        with open("system_messages/sentences.md", "r", encoding="utf-8") as f:
            # Reads lines, strips whitespace, removes empty lines
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        # Fallback message if sentences.md is missing
        messages = ["Focus on your goals."]

    state = {"current_sentence": "", "start_time": 0.0}

    # UI ELEMENTS
    sentence_label = tk.Label(frame, text="", font=("Arial", 24), bg="blue", fg="white")
    sentence_label.pack(pady=20)

    sentence_entry = tk.Entry(frame, font=("Arial", 16))
    sentence_entry.pack(pady=10)

    result_label = tk.Label(frame, text="", font=("Arial", 16), bg="blue", fg="white")
    result_label.pack(pady=20)

    def get_new_sentence():
        # Pick a sentence
        state["current_sentence"] = random.choice(messages)
        sentence_label.config(text=state["current_sentence"])
        sentence_entry.delete(0, tk.END)
        state["start_time"] = time.time()

    def check_sentence(event):
        typed_sentence = sentence_entry.get().strip()
        
        if typed_sentence == state["current_sentence"]:
            elapsed_time = time.time() - state["start_time"] # Calculate WPM by taking the number of words (characters/5) and dividing by the time
            words_count = len(state["current_sentence"]) / 5 # Average word length is considered 5 characters for WPM calculation
            minutes = elapsed_time / 60
            wpm = int(words_count / minutes) if minutes > 0 else 0 # Avoid division by zero
            
            result_label.config(text=f"Your results: {wpm} WPM", fg="lightgreen")
            app.root.after(1500, get_new_sentence)
        else:
            result_label.config(text="Please try again, otherwise thou shalt not pass.", fg="red")

    sentence_entry.bind("<Return>", check_sentence)
    
    # Start the first word
    get_new_sentence()

    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        # Import inside of function (to prevent circular import error)
        from system_functions.squares.inner_menus.skill_training_menu import show_skill_menu
        frame.destroy()
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