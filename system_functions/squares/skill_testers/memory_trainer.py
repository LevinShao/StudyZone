import tkinter as tk
from tkinter import *
from math import sqrt
from random import shuffle
from system_functions.backend.ui_helpers import bind_exit_inner_menu

# Special thanks to VasTheCoder for the original code!
# The code below is a forked and edited version of the original code, some things were changed to suit the program better
# https://vasthecoder.hashnode.dev/memory-game-using-tkinter
# https://github.com/VasTheCoder/Miscellaneous-Projects/blob/main/memory.py

def show_memory_trainer(app):
    app.clear()
    
    # Global/State variables for the game
    NUMBER = 18
    matches = [x for x in range(NUMBER) for _ in range(2)]
    shuffle(matches)
    chances = 30
    won = 0
    answer_list = []
    waiting_for_reset = False
        
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="Memory Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Chances Label
    chances_label = Label(frame, text=f"chances = {chances}", font=("Helvetica", 20), bg=app.BG_CARD, fg=app.TEXT)
    chances_label.pack(pady=10)
    status_label = Label(frame, text="Find all matching pairs!", font=("Helvetica", 14), bg=app.BG_CARD, fg="#94a3b8")
    status_label.pack(pady=(0, 10))

    # Function to determine the number of rows and columns for the grid based on the total number of tiles
    def find_rows_cols(number):
        max_cols = int(sqrt(number))
        cols = max_cols

        for i in range(max_cols, 0, -1):
            if number % i == 0:
                cols = i
                break

        rows = int(number / cols)
        return rows, cols

    rows, cols = find_rows_cols(len(matches))

    def reset():
        nonlocal matches, won, chances, answer_list, waiting_for_reset

        chances = 30
        won = 0
        waiting_for_reset = False
        shuffle(matches)
        answer_list = []
        chances_label["text"] = f"chances = {chances}"
        status_label["text"] = "Find all matching pairs!"

        for tile in tiles:
            # Reset each tile's text and state
            tile["text"] = ' '
            tile["state"] = NORMAL

    def onclick(index):
        nonlocal answer_list, won, chances, waiting_for_reset

        if chances <= 0 or waiting_for_reset:
            return

        # Check if click is valid
        if tiles[index]["text"] == ' ' and len(answer_list) < 2:
            tiles[index]["text"] = str(matches[index])
            answer_list.append(index)

        if len(answer_list) == 2:
            app.root.update()  # Force UI update 

            # If two tiles match
            if matches[answer_list[0]] == matches[answer_list[1]]:
                tiles[answer_list[0]]["state"] = DISABLED
                tiles[answer_list[1]]["state"] = DISABLED
                won += 1

                if won == NUMBER:
                    chances_label["text"] = "You Won!"
                    status_label.config(text="🎉 Congratulations!", fg="#f59e0b")
                else:
                    chances_label["text"] = f"chances = {chances}"
                    status_label.config(text="✅ It's a Match!", fg="#22c55e")

                answer_list = []
            else:
                # If they do not match
                chances -= 1
                chances_label["text"] = f"chances = {chances}"
                status_label.config(text="❌ Not a match. Try again.", fg="#f87171")

                # Reset tiles after incorrect guess
                first_tile = answer_list[0]
                second_tile = answer_list[1]
                answer_list = []
                waiting_for_reset = True

                def hide_tiles():
                    nonlocal waiting_for_reset

                    tiles[first_tile]["text"] = ' '
                    tiles[second_tile]["text"] = ' '

                    waiting_for_reset = False

                    if chances <= 0:
                        for tile in tiles:
                            tile["state"] = DISABLED

                        chances_label["text"] = "You Lost D:"
                        status_label.config(text="💀 Out of chances.", fg="#f87171")

                app.root.after(1250, hide_tiles)

    # Dedicated grid frame to separate pack and grid layout managers
    grid_frame = Frame(frame, bg=app.BG_CARD)
    grid_frame.pack(pady=10)

    # Defining the tiles
    tiles = []
    for i in range(len(matches)):
        btn = Button(grid_frame, text=' ', font=("Helvetica", 40), height=1, width=3, command=lambda i=i: onclick(i))
        tiles.append(btn)

    # Adding the tiles to screen using Grid inside the sub-frame
    for i, tile in enumerate(tiles):
        r = i // cols
        c = i % cols
        tile.grid(row=r, column=c, padx=5, pady=5)

    # Menu Setup
    my_menu = Menu(app.root)
    app.root.config(menu=my_menu)
    option_menu = Menu(my_menu, tearoff=False)
    option_menu.add_command(label="Reset Game", command=reset)
    option_menu.add_separator()
    option_menu.add_command(label="Exit Game", command=app.root.quit)

    # EXIT BUTTON
    def exit_btn():
        from system_functions.squares.inner_menus.skill_training_menu import show_skill_menu
        bind_exit_inner_menu(app, show_skill_menu)

    exit_btn()