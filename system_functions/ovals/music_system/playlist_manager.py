import tkinter as tk
from tkinter import filedialog # Import filedialog for selecting music files
import random
import os
from system_functions.backend.ui_helpers import create_small_button, bind_exit_inner_menu

def show_playlist_manager(app):
    app.clear()

    # Main outer frame
    frame = tk.Frame(app.root, bg=app.BG_CARD, padx=80, pady=40)
    frame.pack(expand=True)

    tk.Label(frame, text="Music Playlist", font=("Segoe UI", 22, "bold"), bg=app.BG_CARD, fg=app.TEXT).pack(pady=10)

    listbox = tk.Listbox(frame, width=60, height=12)
    listbox.pack(pady=20)

    def refresh():
        # Refresh the listbox with the current playlist
        listbox.delete(0, tk.END)
        for song in app.playlist:
            listbox.insert(tk.END, os.path.basename(song))

    def add_song():
        # Add song to playlist using file dialog, then refresh the listbox to show the new song
        file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file:
            app.playlist.append(file)
            refresh()

    def remove_song():
        # Remove selected song from playlist, then refresh the listbox to reflect the change
        selected = listbox.curselection()
        if selected:
            app.playlist.pop(selected[0])
            refresh()

    def play_selected():
        # Play the selected song from the playlist
        selected = listbox.curselection()
        if selected:
            song = app.playlist[selected[0]]
            app.play_music(song)
    
    def play_random_song():
        # Play a random song from the playlist
        if app.playlist:
            random_song = random.choice(app.playlist)
            app.play_music(random_song)

    # EXIT BUTTON FUNCTIONS
    def exit_btn():
        from system_functions.ovals.music_system.music_settings import show_music_player
        bind_exit_inner_menu(app, show_music_player)

    btn_frame = tk.Frame(frame, bg=app.BG_CARD)
    btn_frame.pack(pady=20)

    # Buttons
    create_small_button(btn_frame, "Add Song", add_song, app, primary=True).grid(row=0, column=0, padx=15, pady=15)
    create_small_button(btn_frame, "Remove Song", remove_song, app, primary=True).grid(row=0, column=1, padx=15, pady=15)
    create_small_button(btn_frame, "Play Selected", play_selected, app, primary=False).grid(row=1, column=0, padx=15, pady=10)
    create_small_button(btn_frame, "Play Random", play_random_song, app, primary=False).grid(row=1, column=1, padx=15, pady=10)

    # INITIALIZATION
    exit_btn()
    refresh()