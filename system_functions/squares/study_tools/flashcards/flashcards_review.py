import tkinter as tk
import random
from system_functions.backend.ui_helpers import create_small_button, bind_exit_inner_menu

def review_flashcards(app, flashcards):
    # Mostly made using list structures
    if not flashcards: 
        # If there are no flashcards, just return to the main flashcards menu
        return

    app.clear()

    # Use lists for current_index and showing_answer so they can be modified inside nested functions
    current_index = [0]
    showing_answer = [False]

    # Frames
    # There are two main frames, one for the card display and one for the buttons and progress label below
    review_frame = tk.Frame(app.root, bg=app.BG_MAIN)
    review_frame.pack(fill="both", expand=True)

    card_frame = tk.Frame(review_frame, bg=app.BG_CARD, width=700, height=400)
    card_frame.pack(expand=True)
    card_frame.pack_propagate(False)

    # Text on the card
    card_text = tk.Label(card_frame, text="", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT, wraplength=600, justify="center")
    card_text.pack(expand=True)

    # Progress Label
    progress_label = tk.Label(review_frame, text="", font=("Segoe UI", 14), bg=app.BG_MAIN, fg=app.TEXT)
    progress_label.pack(pady=20)

    # Update Card Display
    def update_card():
        # Get the current card based on the current index
        card = flashcards[current_index[0]]

        if showing_answer[0]:
            # If showing answer, display the answer text.
            card_text.config(text=card["answer"])
        else:
            # Otherwise, show the question.
            card_text.config(text=card["question"])

        # Update the progress label to show current card number and total cards
        progress_label.config(text=f"Card {current_index[0] + 1} / {len(flashcards)}")

    # Flip Card Function
    def flip_card(event=None):
        # Toggle the showing_answer state and update the card display
        showing_answer[0] = not showing_answer[0]
        update_card()

    # Next Card Function
    def next_card():
        # Move to the next card index, wrapping around to the start if at the end
        current_index[0] = (current_index[0] + 1) % len(flashcards) # Use modulus to wrap around
        showing_answer[0] = False
        update_card()

    # Previous Card Function
    def prev_card():
        current_index[0] = (current_index[0] - 1) % len(flashcards) # Use modulus to wrap around (backwards)
        showing_answer[0] = False
        update_card()

    # Shuffle Cards Function
    def shuffle_cards():
        if len(flashcards) <= 1: 
            # Don't shuffle if there is only one card or less
            return
        
        # pick random new index different from current
        current = current_index[0]
        new_index = current

        while new_index == current:
            new_index = random.randint(0, len(flashcards) - 1)

        # Update current index to the new random index and reset to showing question
        current_index[0] = new_index
        showing_answer[0] = False

        update_card()

    # Click to flip bindings on both the card frame and the text so that clicking anywhere on the card flips it
    card_frame.bind("<Button-1>", flip_card)
    card_text.bind("<Button-1>", flip_card)

    # Buttons
    btn_frame = tk.Frame(review_frame, bg=app.BG_MAIN)
    btn_frame.pack(pady=30)

    create_small_button(btn_frame, "Previous", prev_card, app, primary=True).grid(row=0, column=0, padx=20)
    create_small_button(btn_frame, "Next", next_card, app, primary=True).grid(row=0, column=1, padx=20)
    create_small_button(btn_frame, "Shuffle", shuffle_cards, app, primary=False).grid(row=0, column=2, padx=20)

    # EXIT BUTTON FUNCTIONS
    def exit_btn():
        from system_functions.squares.study_tools.flashcards.flashcards_main import show_flashcards
        bind_exit_inner_menu(app, show_flashcards)

    exit_btn()
    update_card() # Initial card display