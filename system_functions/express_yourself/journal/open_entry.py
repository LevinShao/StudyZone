import tkinter as tk
from system_functions.backend.ui_helpers import *
from db_files.data_manager import get_user_data, update_user_data

def open_journal_entry(app, index):
    app.clear()

    user_data = get_user_data(app.current_user)
    journal_entries = user_data["journal_entries"]

    entry = journal_entries[index]

    container = tk.Frame(app.root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    # Main Card
    card = tk.Frame(container, bg=BG_CARD, padx=30, pady=30)
    card.pack(fill="both", expand=True, padx=50, pady=40)

    # MAIN TITLE
    tk.Label(card, text="Title", font=("Segoe UI", 11), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    title_edit = tk.Entry(card, font=("Segoe UI", 12), bg="#111827", fg="white", insertbackground="white")
    title_edit.pack(fill="x", pady=(5, 15), ipady=5)
    title_edit.insert(0, entry["title"]) # Insert the title of the journal entry into the title edit field

    # INFORMATION FRAME
    info_frame = tk.Frame(card, bg=BG_CARD)
    info_frame.pack(fill="x", pady=(0, 20))

    # WEATHER
    weather_frame = tk.Frame(info_frame, bg=BG_CARD)
    weather_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

    tk.Label(weather_frame, text="Weather", font=("Segoe UI", 11), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    weather_edit = tk.Entry(weather_frame, font=("Segoe UI", 11), bg="#111827", fg="white", insertbackground="white")
    weather_edit.pack(fill="x", ipady=5)
    weather_edit.insert(0, entry["weather"])

    # TEMPERATURE
    temp_frame = tk.Frame(info_frame, bg=BG_CARD)
    temp_frame.pack(side="left", fill="x", expand=True, padx=(10, 10))

    tk.Label(temp_frame, text="Temperature", font=("Segoe UI", 11), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    temp_edit = tk.Entry(temp_frame, font=("Segoe UI", 11), bg="#111827", fg="white", insertbackground="white")
    temp_edit.pack(fill="x", ipady=5)
    temp_edit.insert(0, entry["temperature"])

    # EMOTION
    emotion_frame = tk.Frame(info_frame, bg=BG_CARD)
    emotion_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

    tk.Label(emotion_frame, text="Emotion", font=("Segoe UI", 11), bg=BG_CARD, fg=TEXT).pack(anchor="w")

    emotion_edit = tk.Entry(emotion_frame, font=("Segoe UI", 11), bg="#111827", fg="white", insertbackground="white")
    emotion_edit.pack(fill="x", ipady=5)
    emotion_edit.insert(0, entry["emotion"])

    # DATE
    tk.Label(card, text=f"Date: {entry['date']}", font=("Segoe UI", 11, "bold"), bg=BG_CARD, fg="#94a3b8").pack(anchor="w", pady=(0, 20))

    # CONTENTS
    text_box = tk.Text(card, font=("Segoe UI", 12), bg="#111827", fg="white", wrap="word", insertbackground="white")
    text_box.pack(fill="both", expand=True)
    text_box.insert("1.0", entry["content"])

    # We must start in read-only mode, and we need a mutable variable to track whether we're in edit mode or not for the toggle_edit function
    editing = [False]

    def set_read_only():
        title_edit.config(state="disabled")
        weather_edit.config(state="disabled")
        temp_edit.config(state="disabled")
        emotion_edit.config(state="disabled")
        text_box.config(state="disabled")

    def set_editable():
        title_edit.config(state="normal")
        weather_edit.config(state="normal")
        temp_edit.config(state="normal")
        emotion_edit.config(state="normal")
        text_box.config(state="normal")

    set_read_only()

    # Edit / Save Changes
    def toggle_edit():

        # Enter Edit Mode
        if not editing[0]:
            editing[0] = True
            set_editable()
            edit_btn.config(text="Save Changes")

        # Save Changes and Exit Edit Mode
        else:
            entry["title"] = title_edit.get().strip()
            entry["weather"] = weather_edit.get().strip()
            entry["temperature"] = temp_edit.get().strip()
            entry["emotion"] = emotion_edit.get().strip()
            entry["content"] = text_box.get("1.0", tk.END).strip()

            update_user_data(app.current_user, user_data)
            editing[0] = False
            set_read_only()
            edit_btn.config(text="Edit Entry")

    # Delete Entry
    def delete_entry():
        from system_functions.express_yourself.journal.view_your_entries import show_entries

        journal_entries.pop(index)
        update_user_data(app.current_user, user_data)
        show_entries(app)

    # Buttons
    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.pack(pady=20)

    edit_btn = create_small_button(btn_frame, "Edit Entry", toggle_edit, app, primary=True)
    edit_btn.grid(row=0, column=0, padx=10)

    create_small_button(btn_frame, "Delete Entry", delete_entry, app, primary=False).grid(row=0, column=1, padx=10)

    # Exit Button
    def exit_to_entries(event=None):
        from system_functions.express_yourself.journal.view_your_entries import show_entries

        app.root.unbind("<Escape>")
        show_entries(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_entries)
    app.root.bind("<Escape>", exit_to_entries)