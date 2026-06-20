import tkinter as tk
from datetime import datetime
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data
from system_functions.squares.mindfulness.wellbeing_journal.view_your_entries import show_entries

def create_new_entry(app):
    app.clear()

    user_data = get_user_data(app.current_user)
    journal_entries = user_data["journal_entries"]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Journal", font=("Segoe UI", 28, "bold"), fg=TEXT, bg=BG_MAIN).pack(pady=30)

    # Main Card
    card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    card.pack(fill="both", expand=True, padx=60, pady=(0, 20))

    # Current Date is automatically added to each entry and cannot be edited by the user
    current_date = datetime.now().strftime("%d %B %Y")
    tk.Label(card, text=f"Date: {current_date}", font=("Segoe UI", 12, "bold"), bg=BG_CARD, fg="#94a3b8").pack(anchor="w", pady=(0, 20))

    # Title and Info Inputs
    tk.Label(card, text="Title", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")
    title_entry = tk.Entry(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    title_entry.pack(fill="x", pady=(5, 15), ipady=6)

    top_inputs = tk.Frame(card, bg=BG_CARD)
    top_inputs.pack(fill="x", pady=(0, 20))

    # WEATHER
    weather_frame = tk.Frame(top_inputs, bg=BG_CARD)
    weather_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

    tk.Label(weather_frame, text="Weather", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    weather_entry = tk.Entry(weather_frame, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    weather_entry.pack(fill="x", ipady=5)

    # TEMPERATURE
    temp_frame = tk.Frame(top_inputs, bg=BG_CARD)
    temp_frame.pack(side="left", fill="x", expand=True, padx=(10, 10))

    tk.Label(temp_frame, text="Temperature", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    temp_entry = tk.Entry(temp_frame, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    temp_entry.pack(fill="x", ipady=5)

    # EMOTION AT THE TIME OF WRITING
    emotion_frame = tk.Frame(top_inputs, bg=BG_CARD)
    emotion_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

    tk.Label(emotion_frame, text="Emotion", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    emotion_entry = tk.Entry(emotion_frame, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    emotion_entry.pack(fill="x", ipady=5)

    # MAIN CONTENT
    tk.Label(card, text="Journal Entry", font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    content_text = tk.Text(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white", wrap="word", height=22)
    content_text.pack(fill="x", pady=(5, 50))

    # Clear all input fields
    def clear_fields():
        # Used for the new entry button
        title_entry.delete(0, tk.END)
        weather_entry.delete(0, tk.END)
        temp_entry.delete(0, tk.END)
        emotion_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END) # use 1.0 to delete from the start of the text box to the end

    def save_entry():
        # Get all the data from the fields and save it as a new journal entry in the user's data, then clear the fields for a new entry
        title = title_entry.get().strip()
        weather = weather_entry.get().strip()
        temp = temp_entry.get().strip()
        emotion = emotion_entry.get().strip()
        content = content_text.get("1.0", tk.END).strip()

        if title == "" and content == "": 
            # at minimum, there should be a title or some content to save an entry
            # Weather, temperature, and emotion can be left blank if the user doesn't want to fill them out
            return

        # Append the new entry to the user's journal entries and update the user data
        journal_entries.append({
            "title": title,
            "weather": weather,
            "temperature": temp,
            "emotion": emotion,
            "content": content,
            "date": current_date
        })

        update_user_data(app.current_user, user_data)
        clear_fields() # Clear fields after saving the entry

    # Buttons
    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.pack()

    create_small_button(btn_frame, "Save Entry", save_entry, app, primary=True).grid(row=0, column=0, padx=15)
    create_small_button(btn_frame, "New Entry", clear_fields, app, primary=True).grid(row=0, column=1, padx=15)
    create_small_button(btn_frame, "View Previous Entries", lambda: show_entries(app), app, primary=False).grid(row=0, column=2, padx=15)

    # Exit Button
    def exit_to_mindful_menu(event=None):
        from system_functions.squares.inner_menus.mindfulness import show_mindfulness

        app.root.unbind("<Escape>")
        show_mindfulness(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_mindful_menu)
    app.root.bind("<Escape>", exit_to_mindful_menu)