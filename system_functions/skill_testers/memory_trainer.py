import tkinter as tk
from tkinter import *
from tkinter import messagebox
from math import sqrt
from random import shuffle

def show_memory_trainer(app):
    app.clear()
    
    # Global/State variables for the game
    NUMBER = 18
    matches = [x for x in range(NUMBER) for _ in range(2)]
    shuffle(matches)
    chances = 30
    won = 0
    answer_list = []
    
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))
    title_label = tk.Label(top_bar, text="Memory Trainer", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    label = Label(frame, text=f"chances = {chances}", font=("Helvetica", 20), bg=app.BG_CARD, fg=app.TEXT)
    label.pack(pady=10)

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
        nonlocal matches, won, chances, answer_list
        chances = 30
        won = 0
        shuffle(matches)
        answer_list = []
        label["text"] = f"chances = {chances}"
        for tile in tiles:
            tile["text"] = ' '
            tile["state"] = NORMAL

    def onclick(index):
        nonlocal answer_list, won, chances
        if chances <= 0:
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
                    label["text"] = "You Won!"
                else:
                    label["text"] = f"It's a Match! chances = {chances}"
                answer_list = []
            else:
                # If they do not match
                chances -= 1
                label["text"] = f"Ahhh try again, chances = {chances}"
                messagebox.showinfo("Incorrect", "Incorrect")
                
                # Reset tiles after incorrect guess
                tiles[answer_list[0]]["text"] = ' '
                tiles[answer_list[1]]["text"] = ' '
                answer_list = []
                
                if chances <= 0:
                    for tile in tiles:
                        tile["state"] = DISABLED
                    label["text"] = "You Lost D:"

    # NEW: Dedicated grid frame to separate pack and grid layout managers
    grid_frame = Frame(frame, bg=app.BG_CARD)
    grid_frame.pack(pady=10)

    # Defining the tiles
    tiles = []
    for i in range(len(matches)):
        # Notice we changed the parent container to 'grid_frame'
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
    my_menu.add_cascade(label="Options", menu=option_menu)
    option_menu.add_command(label="Reset Game", command=reset)
    option_menu.add_separator()
    option_menu.add_command(label="Exit Game", command=app.root.quit)

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