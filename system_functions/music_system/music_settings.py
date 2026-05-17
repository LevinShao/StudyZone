import tkinter as tk
from tkinter import ttk
import pygame # Import pygame for music playback functionality
from system_functions.backend.ui_helpers import bind_exit_menu
from system_functions.music_system.playlist_manager import show_playlist_manager

def show_music_player(app):
    app.clear()

    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=100, pady=100)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Currently Playing:\n\n{app.current_song.split('/')[-1]}", font=("Segoe UI", 18), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)

    def set_volume(value):
        # Volume slider callback to set the music volume in pygame
        app.volume = float(value) / 100
        pygame.mixer.music.set_volume(app.volume)

    # Main volume slider
    volume_slider = ttk.Scale(frame, from_=0, to=100, orient="horizontal", command=set_volume)
    volume_slider.set(app.volume * 100)
    volume_slider.pack(pady=10)

    def pause():
        # Pause or resume the music playback
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def restart():
        # Restart the current song from the beginning
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()

    def view_playlist():
        # Go to playlist manager screen
        show_playlist_manager(app)

    # Buttons
    tk.Button(frame, text="Pause / Resume", command=pause, bg=app.ACCENT, fg=app.TEXT, width=20).pack(pady=10)
    tk.Button(frame, text="Restart Song", command=restart, bg=app.ACCENT, fg=app.TEXT, width=20).pack(pady=10)
    tk.Button(frame, text="View Playlist", command=view_playlist, bg=app.ACCENT, fg=app.TEXT, width=20).pack(pady=10)
    tk.Button(frame, text="← Back", command=app.show_main_menu, bg=app.BG_CARD, fg=app.TEXT, width=20).pack(pady=10)

    # Exit Button
    bind_exit_menu(app)