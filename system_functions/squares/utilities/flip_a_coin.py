import tkinter as tk
import random
from PIL import Image, ImageTk
from system_functions.backend.ui_helpers import *

# perhaps the easiest tool i've made for this app, took around only 20 mins to create

def coinflip(app):
    app.clear()

    # Main Frame
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Coin Flipper", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)

    # Load Images
    heads_image = Image.open("img_assets/coin_sides/heads.png") # Open the image
    heads_resize = heads_image.resize((500, 500)) # Make the image bigger
    heads = ImageTk.PhotoImage(heads_resize) # New image

    tails_image = Image.open("img_assets/coin_sides/tails.png")
    tails_resize = tails_image.resize((500, 500))
    tails = ImageTk.PhotoImage(tails_resize)

    # Image Display
    coin_label = tk.Label(frame, image=heads, bg=app.BG_CARD) # Initially the screen will display heads
    # Do this because otherwise the image will be garbage collected meaning that the label will not update
    # Garbage collection occurs because the image is not referenced anywhere else meaning that it is not needed
    coin_label.image = heads
    coin_label.pack(pady=20)

    # Result Label
    result_label = tk.Label(frame, text="Press the button to flip the coin!", font=("Segoe UI", 14), bg=app.BG_CARD, fg=app.TEXT)
    result_label.pack(pady=15)

    def flip_coin():
        # 0 or 1 heads or tails, it's as simple as that
        num = random.randint(0, 1) # Generate a random number between 0 and 1

        if num == 0:
            coin_label.config(image=heads)
            coin_label.image = heads # Do this because otherwise the image will be garbage collected meaning that the label will not update
            result_label.config(text="It's HEADS!")
        else:
            coin_label.config(image=tails)
            coin_label.image = tails # Do this because otherwise the image will be garbage collected meaning that the label will not update
            result_label.config(text="It's TAILS!")

    flip_btn = tk.Button(frame, text="Flip Coin", font=("Segoe UI", 14, "bold"), bg=app.ACCENT, fg="white", 
                         activebackground=app.ACCENT_HOVER, command=flip_coin, padx=20, pady=10)
    flip_btn.pack(pady=20)

    # EXIT BUTTON FUNCTIONS
    def exit_to_studymenu(event=None):
        from system_functions.squares.inner_menus.utilities import show_utilities

        app.root.unbind("<Escape>")
        show_utilities(app)

    hover_on = lambda e: exit_btn.config(bg=app.ACCENT_HOVER)
    hover_off = lambda e: exit_btn.config(bg=app.ACCENT)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Enter>", hover_on)
    exit_btn.bind("<Leave>", hover_off)
    exit_btn.bind("<Button-1>", exit_to_studymenu)
    app.root.bind("<Escape>", exit_to_studymenu)