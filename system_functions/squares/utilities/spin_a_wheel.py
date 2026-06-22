import tkinter as tk
import random
import math
from system_functions.backend.ui_helpers import *

# CODE INSPIRED BY GEEKSFORGEEKS TUTORIAL

def spin_a_wheel(app):
    app.clear()

    # Core prize list & colors (made mutable)
    final = []
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3', '#33FFF0']

    # Core animation variables
    current_angle = 0
    speed = 0
    is_spinning = False

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="Wheel of Choices", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Setup Canvas for drawing the wheel
    canvas = tk.Canvas(frame, width=400, height=400, bg=app.BG_CARD)
    canvas.pack(pady=10)

    # Result Display Label
    result_label = tk.Label(frame, text='Click Spin to Play!', font=('Segoe UI', 16, 'bold'))
    result_label.pack(pady=5)

    # Input Frame for Users to Add Options
    input_frame = tk.Frame(frame)
    input_frame.pack(pady=5)

    entry_label = tk.Label(input_frame, text="Add Option:", font=('Segoe UI', 10))
    entry_label.pack(side=tk.LEFT, padx=5)

    prize_entry = tk.Entry(input_frame, font=('Segoe UI', 10))
    prize_entry.pack(side=tk.LEFT, padx=5)

    def add_custom_option():
        nonlocal colors  # use nonlocal to access outside scope safely
        new_prize = prize_entry.get().strip() # Fetch new prize

        if new_prize:
            final.append(new_prize) # Add new prize to list
            random_color = f"#{random.randint(0, 0xFFFFFF):06x}" # Generate a random hex color for the new slice
            colors.append(random_color) # Add new color to list
            prize_entry.delete(0, tk.END) # Clear entry field
            draw_wheel() # Re-draw the wheel dynamically

    add_button = tk.Button(input_frame, text="Add", font=('Segoe UI', 11), command=add_custom_option)
    add_button.pack(side=tk.LEFT)

    def draw_wheel():
        nonlocal current_angle
        canvas.delete('all') # Clear previous draw

        if not final: 
            # If no prizes added, return
            return
            
        num_slices = len(final) # Number of slices (prizes)
        slice_angle = 360 / num_slices # Angle of each slice in degrees

        for i in range(num_slices):
            start_arc = current_angle + (i * slice_angle) # Start angle of each slice
            canvas.create_arc(50, 50, 350, 350, start=start_arc, extent=slice_angle, fill=colors[i], outline='black', width=2) # Draw each slice
            
            # Calculate exact center of the arc to put text right-side up
            mid_angle = math.radians(start_arc + (slice_angle / 2)) # Mid angle of each slice
            text_x = 200 + 120 * math.cos(mid_angle) # Center x of each slice
            text_y = 200 - 120 * math.sin(mid_angle) # Center y of each slice
            
            canvas.create_text(text_x, text_y, text=final[i], font=('Segoe UI', 10, 'bold'), fill='black') # Draw text on each slice

        # Draw red pointer arrow
        canvas.create_polygon(340, 200, 370, 185, 370, 215, fill='red', outline='black')

    def determine_winner():
        if not final: 
            # If no prizes added, return
            return
        
        num_slices = len(final) # Number of slices (prizes)
        slice_angle = 360 / num_slices # Angle of each slice in degrees
        normalized_angle = (360 - current_angle) % 360 # Normalize angle to 0-360 degrees range
        winning_index = int(normalized_angle / slice_angle) % num_slices # Calculate winning index
        prize_won = final[winning_index] # Get prize won
        result_label.config(text=f'Final Result: {prize_won}!') # Update result label

    def animate_wheel():
        nonlocal current_angle, speed, is_spinning

        if speed > 0.1:
            current_angle = (current_angle + speed) % 360 # Update current angle with speed
            speed *= 0.975 # Decrease speed gradually to stop the wheel
            draw_wheel() # Re-draw the wheel
            app.root.after(20, animate_wheel) # Keep looping while spinning
        else:
            is_spinning = False
            speed = 0 # Ensure speed completely drops to 0
            spin_button.config(state=tk.NORMAL)
            determine_winner() # Determine winner and update result label

    def start_spin():
        nonlocal speed, is_spinning

        if not is_spinning and final:
            is_spinning = True
            spin_button.config(state=tk.DISABLED) # Disable button while spinning
            result_label.config(text='Spinning...')
            speed = random.uniform(45, 60) # Randomize initial speed for variety
            animate_wheel()

    spin_button = tk.Button(frame, text='SPIN WHEEL', font=('Segoe UI', 14, 'bold'), bg='#4CAF50', fg='white', command=start_spin)
    spin_button.pack(pady=10)

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
    
    draw_wheel()