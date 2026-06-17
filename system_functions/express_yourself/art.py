import tkinter as tk
from tkinter import colorchooser, ttk
from tkinter import filedialog
from PIL import ImageGrab   # For saving canvas as image
from system_functions.backend.ui_helpers import *

def art(app):
    app.clear()

    # Major State Variables
    color_fg = "black"   # Default pen color
    color_bg = "white"   # Default bg color
    penwidth = 5         # Default pen width
    
    old_x = None         # Previous x coordinate of mouse (for drawing lines), set to None when not drawing
    old_y = None         # Previous y coordinate of mouse (for drawing lines), set to None when not drawing

    # UNDO / REDO STACKS 
    # Each stroke is a list of line segments, and undo/redo stacks are lists of strokes.
    # When a stroke is completed (mouse released), it's added to the undo stack.
    # Undoing moves the last stroke from undo to redo stack, and redoing moves it back to undo stack.
    undo_stack = []
    redo_stack = []
    current_stroke = []

    # Mainframe
    frame = tk.Frame(app.root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    # Controls
    controls = tk.Frame(frame, bg=BG_CARD, padx=10, pady=10)
    controls.pack(side="left", fill="y")

    tk.Label(controls, text="Pen Width", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=TEXT).pack(pady=(0, 10))

    # Canvas for drawing
    canvas = tk.Canvas(frame, bg=color_bg, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Change Pen Width
    def change_width(value):
        nonlocal penwidth
        penwidth = float(value) # Update penwidth variable with slider value

    # Paint Function
    def paint(event):
        nonlocal old_x, old_y, current_stroke

        if old_x and old_y:
            # Draw a line from the previous mouse position to the current position, and save the line ID in current_stroke
            line = canvas.create_line(old_x, old_y, event.x, event.y, width=penwidth, fill=color_fg, capstyle=tk.ROUND, smooth=True)
            current_stroke.append(line)

        # Update old_x and old_y to the current mouse position for the next line segment
        old_x = event.x
        old_y = event.y

    # Reset Function (called on mouse release to end the current stroke)
    def reset(event):
        nonlocal old_x, old_y, current_stroke

        # Reset old_x and old_y to None to indicate that the stroke has ended
        old_x = None
        old_y = None

        # Save completed stroke
        if current_stroke:
            undo_stack.append(current_stroke)
            current_stroke = []

            # New action clears redo history
            redo_stack.clear()

    # Undo Function
    def undo():
        if not undo_stack:
            return

        last_stroke = undo_stack.pop()

        for line in last_stroke:
            canvas.itemconfigure(line, state="hidden")

        redo_stack.append(last_stroke)

    # Redo Function
    def redo():
        if not redo_stack:
            return

        restored_stroke = redo_stack.pop()

        for line in restored_stroke:
            canvas.itemconfigure(line, state="normal")

        undo_stack.append(restored_stroke)

    # Clear the entire canvas
    def clear_canvas():
        canvas.delete("all")

    # Change Pen Color
    def change_fg():
        nonlocal color_fg

        # Use the Tkinter in-built color chooser dialog to select a color
        color = colorchooser.askcolor(color=color_fg)[1]

        if color:
            # Update the pen color variable with the selected color
            color_fg = color

    # Change Background Color
    def change_bg():
        nonlocal color_bg

        # Use the Tkinter in-built color chooser dialog to select a color
        color = colorchooser.askcolor(color=color_bg)[1]

        if color:
            # Update the background color variable and apply it to the canvas
            color_bg = color
            canvas.config(bg=color_bg)

    # Save the canvas as an image file
    def save_art():
        # Ask user where to save image
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Files", "*.png"),    # Default to PNG format
                ("JPEG Files", "*.jpg"),   # Allow user to choose JPG / JPEG if they want
                ("All Files", "*.*")       # Allow user to choose any file type if they want
            ]
        )

        if not file_path: 
            # User cancelled save dialog
            return

        # Get canvas position on screen
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()

        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()

        # Screenshot only canvas area
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

    # Small Undo/Redo Buttons with Hover Effects
    undo_redo_frame = tk.Frame(controls, bg=BG_CARD)
    undo_redo_frame.pack(pady=10)

    undo_btn = tk.Label(undo_redo_frame, text="↶ Undo", bg="#374151", fg="white", font=("Segoe UI", 10, "bold"), width=10, height=1, cursor="hand2")
    undo_btn.pack(side="left", padx=5)

    redo_btn = tk.Label(undo_redo_frame, text="↷ Redo", bg="#374151", fg="white", font=("Segoe UI", 10, "bold"), width=10, height=1, cursor="hand2")
    redo_btn.pack(side="left", padx=5)

    # Main Hover Effects
    def undo_hover_on(e): 
        undo_btn.config(bg="#4b5563")
        
    def undo_hover_off(e):
        undo_btn.config(bg="#374151")

    def redo_hover_on(e): 
        redo_btn.config(bg="#4b5563")

    def redo_hover_off(e): 
        redo_btn.config(bg="#374151")

    undo_btn.bind("<Enter>", undo_hover_on)
    undo_btn.bind("<Leave>", undo_hover_off)
    undo_btn.bind("<Button-1>", lambda e: undo())
    redo_btn.bind("<Enter>", redo_hover_on)
    redo_btn.bind("<Leave>", redo_hover_off)
    redo_btn.bind("<Button-1>", lambda e: redo())

    # Pen Width Slider
    slider = ttk.Scale(controls, from_=1, to=50, orient="vertical", command=change_width)
    slider.set(penwidth)
    slider.pack(pady=20, ipadx=10, fill="y", expand=True)

    # Buttons
    create_small_button(controls, "Brush Color", change_fg, app, primary=True).pack(pady=10)
    create_small_button(controls, "Background", change_bg, app, primary=True).pack(pady=10)
    create_small_button(controls, "Clear Canvas", clear_canvas, app, primary=True).pack(pady=10)
    create_small_button(controls, "Save Art", save_art, app, primary=False).pack(pady=10)

    # Drawing Bindings
    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<ButtonRelease-1>", reset)
    app.root.bind("<Control-z>", lambda e: undo())
    app.root.bind("<Control-y>", lambda e: redo())

    # Exit Button
    def exit_to_express_menu(event=None):
        from system_functions.inner_menus.express_yourself_menu import show_express_menu

        app.root.unbind("<Escape>")
        show_express_menu(app)

    exit_btn = tk.Label(app.root, text="←", bg="#ef4444", fg="white", font=("Segoe UI", 18, "bold"), cursor="hand2")
    exit_btn.place(x=30, y=30)
    exit_btn.lift()
    exit_btn.bind("<Button-1>", exit_to_express_menu)
    app.root.bind("<Escape>", exit_to_express_menu)