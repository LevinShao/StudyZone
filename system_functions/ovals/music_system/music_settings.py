import tkinter as tk
import customtkinter as ctk
import pygame # Import pygame for music playback functionality
from system_functions.backend.ui_helpers import bind_exit_menu, create_small_button
from system_functions.ovals.music_system.playlist_manager import show_playlist_manager

def show_music_player(app):
    app.clear()

    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=100, pady=100)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Currently Playing:\n\n{app.current_song.split('/')[-1]}", font=("Segoe UI", 18), bg=app.BG_CARD, fg=app.TEXT).pack(pady=20)

    def set_volume(value):
        # Volume slider callback to set the music volume in pygame
        app.volume = float(value) / 100
        pygame.mixer.music.set_volume(app.volume)

    # Updated CTk volume slider
    volume_slider = ctk.CTkSlider(frame, from_=0, to=100,  width=300, height=16, corner_radius=8, button_color="#4a90e2", 
                                  button_hover_color="#357abd", progress_color="#4a90e2", fg_color="#2b2b2b", command=set_volume)
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
        show_playlist_manager(app) # Go to playlist manager screen

    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)

    # Buttons
    create_small_button(btn_frame, "Pause / Resume", pause, app, primary=True).grid(row=0, column=0, padx=15, pady=15)
    create_small_button(btn_frame, "Restart Song", restart, app, primary=True).grid(row=1, column=0, padx=15, pady=15)
    create_small_button(btn_frame, "View Playlist", view_playlist, app, primary=False).grid(row=2, column=0, padx=15, pady=(10, 0))

    # Exit Button
    bind_exit_menu(app)