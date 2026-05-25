import tkinter as tk
from system_functions.flashcards.flashcards_review import review_flashcards
from system_functions.backend.ui_helpers import create_small_button, create_field, bind_exit_menu
from db_files.data_manager import get_user_data, update_user_data

def show_flashcards(app):
    app.clear()

    # Load flashcards from user data
    user_data = get_user_data(app.current_user)
    flashcards = user_data["flashcards"]

    # Outer frames
    outer = tk.Frame(app.root, bg=app.BG_MAIN)
    outer.pack(fill="both", expand=True)

    frame = tk.Frame(outer, bg=app.BG_CARD, padx=40, pady=40)
    frame.pack(expand=True)

    # Title
    tk.Label(frame, text="Flashcards", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)

    # Input fields
    question_entry, _ = create_field(frame, "Question")
    answer_entry, _ = create_field(frame, "Answer")

    # Listbox for flashcard display
    listbox = tk.Listbox(frame, width=60, height=10)
    listbox.pack(pady=20)

    # Refresh function to update list box
    def refresh():
        listbox.delete(0, tk.END) # Clear the list box before repopulating

        for card in flashcards:
            # Only show the question in the list box, answer is revealed in review or edit popup
            listbox.insert(tk.END, card["question"])

    # Add Flashcard
    def add_flashcard():
        # Input validation to ensure question and answer are not empty
        # Error handling messages for this will be added later
        question = question_entry.get().strip()
        answer = answer_entry.get().strip()

        if question == "" or answer == "":
            return

        # Add the new flashcard to the user's data and refresh the list box
        flashcards.append({"question": question, "answer": answer})
        update_user_data(app.current_user, user_data)

        # Clear the input fields after adding
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)

        refresh()

    # Delete Flashcard
    def delete_flashcard():
        # Get the selected flashcard index from the list box
        selected = listbox.curselection()

        if not selected:
            return

        # Remove the selected flashcard from the user's data and refresh the list box
        flashcards.pop(selected[0])
        update_user_data(app.current_user, user_data)

        refresh()

    # Edit Flashcard
    def edit_flashcard():
        selected = listbox.curselection()

        if not selected:
            return

        # Get the selected flashcard data to pre-fill the edit popup fields
        index = selected[0]
        card = flashcards[index]

        # Popup Window
        edit_win = tk.Toplevel(app.root)
        edit_win.title("Edit Flashcard")
        edit_win.configure(bg=app.BG_CARD)

        tk.Label(edit_win, text="Edit Flashcard", font=("Segoe UI", 16, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

        # Question
        tk.Label(edit_win, text="Question", bg=app.BG_CARD, fg=app.TEXT).pack(anchor="w", padx=20)

        question_entry_popup = tk.Entry(edit_win, width=50)
        question_entry_popup.insert(0, card["question"])
        question_entry_popup.pack(padx=20, pady=5)

        # Answer
        tk.Label(edit_win, text="Answer", bg=app.BG_CARD, fg=app.TEXT).pack(anchor="w", padx=20)

        answer_entry_popup = tk.Entry(edit_win, width=50)
        answer_entry_popup.insert(0, card["answer"])
        answer_entry_popup.pack(padx=20, pady=5)

        # Save Edited Changes function
        def save_changes():
            card["question"] = (question_entry_popup.get())
            card["answer"] = (answer_entry_popup.get())

            update_user_data(app.current_user, user_data)
            refresh()
            edit_win.destroy()

        create_small_button(edit_win, "Save Changes", save_changes, app, primary=True).pack(pady=15)

    # Show the Review Menu
    def show_review_menu():
        review_flashcards(app, flashcards)

    # Buttons
    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)

    # Row 1
    create_small_button(btn_frame, "Add Flashcard", add_flashcard, app, primary=False).grid(row=0, column=0, padx=15, pady=15)
    create_small_button(btn_frame, "Edit Flashcard", edit_flashcard, app, primary=False).grid(row=0, column=1, padx=15, pady=15)

    # Row 2
    create_small_button(btn_frame, "Delete Flashcard", delete_flashcard, app, primary=False).grid(row=1, column=0, padx=15, pady=10)
    create_small_button(btn_frame, "Review Flashcards", show_review_menu, app, primary=True).grid(row=1, column=1, padx=15, pady=10)

    # Initialization
    bind_exit_menu(app)
    refresh()