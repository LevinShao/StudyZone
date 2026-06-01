import tkinter as tk
import random
import time

# CREDITS TO YOUTUBE TUTORIAL Code With Don

def show_typing_app(app):
    app.clear()
    
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    words = ["I", "love", "my", "mother", "and", "the", "pet", "dog"]
    state = {"current_word": "", "start_time": 0.0}

    word_label = tk.Label(frame, text="", font=("Arial", 24), bg="blue", fg="white")
    word_label.pack(pady=20)

    word_entry = tk.Entry(frame, font=("Arial", 16))
    word_entry.pack(pady=10)

    result_label = tk.Label(frame, text="", font=("Arial", 16), bg="blue", fg="white")
    result_label.pack(pady=20)

    def get_new_word():
        state["current_word"] = random.choice(words)
        word_label.config(text=state["current_word"])
        word_entry.delete(0, tk.END)
        state["start_time"] = time.time()

    def check_word(event):
        typed_word = word_entry.get().strip()
        if typed_word == state["current_word"]:
            elapsed_time = time.time() - state["start_time"]
            
            words_count = len(state["current_word"]) / 5
            minutes = elapsed_time / 60
            wpm = int(words_count / minutes) if minutes > 0 else 0
            
            result_label.config(text=f"Your results: {wpm} WPM", fg="lightgreen")
            
            app.root.after(1500, get_new_word)
        else:
            result_label.config(text="Please try again, otherwise thou shalt not pass.", fg="red")

    word_entry.bind("<Return>", check_word)
    get_new_word()

    # EXIT BUTTON FUNCTIONS
    def exit_to_skill_menu(event=None):
        # Import inside of function (to prevent circular import error)
        from system_functions.skill_training_menu import show_skill_menu
        frame.destroy() 
        app.root.unbind("<Escape>")
        show_skill_menu(app)

    exit_btn = tk.Label(frame, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_skill_menu)
    app.root.bind("<Escape>", exit_to_skill_menu)