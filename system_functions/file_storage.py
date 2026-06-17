import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from system_functions.backend.ui_helpers import *

def show_file_storage(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)

    # Top Bar with Title
    top_bar = tk.Frame(frame, bg=app.BG_CARD, height=70)
    top_bar.pack(fill="x", pady=(15, 5))

    title_label = tk.Label(top_bar, text="File Storage", font=("Segoe UI", 26, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    # Main Text Area
    text_area = tk.Text(frame, wrap="word", bg=app.BG_CARD, fg=app.TEXT)
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    # Action Button Frame
    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(fill="x", pady=10)

    def save_file():
        file_content = text_area.get("1.0", tk.END).strip()
        
        # Prevent saving empty files unnecessarily
        if not file_content:
            messagebox.showwarning("Warning", "Can't save if there is nothing to save at all!")
            return

        # Trigger native save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                # Save the file to storage
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_content)
                messagebox.showinfo("Success", "File stored successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}") # Fallback

    def open_file():
        # Prompt user to select a target file
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        if file_path:
            try:
                # Open the actual file
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Clear the text area and inject the new data from file
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}") # Fallback

    # Buttons
    create_small_button(btn_frame, "Open From Storage", open_file, app, primary=True).pack(side="left", padx=20)
    create_small_button(btn_frame, "Save to Storage", save_file, app, primary=True).pack(side="right", padx=20)

    bind_exit_menu(app)