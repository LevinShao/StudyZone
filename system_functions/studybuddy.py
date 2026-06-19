# AI ASSISTANT IDEA FOR STUDYZONE
# WILL WORK SIMILAR TO CHATGPT OR AT LEAST I HOPE SO
import tkinter as tk
from system_functions.backend.ui_helpers import *

def show_ai(app):
    app.clear()

    # Mainframe
    frame = tk.Frame(app.root, bg=app.BG_CARD)
    frame.pack(fill="both", expand=True)
    
    coming_soon = tk.Label(frame, text="Coming Soon!", font=("Segoe UI", 24, "bold"), bg=app.BG_CARD, fg=app.TEXT)
    coming_soon.pack(expand=True)

    bind_exit_menu(app)