import tkinter as tk
from tkinter import filedialog # Import filedialog for selecting music files
import os

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

    refresh()

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

    # Buttons
    tk.Button(frame, text="Add Song", command=add_song, bg=app.ACCENT, fg=app.TEXT, width=20).pack(pady=5)
    tk.Button(frame, text="Remove Song", command=remove_song, bg="#334155", fg=app.TEXT, width=20).pack(pady=5)
    tk.Button(frame, text="Play Selected", command=play_selected, bg="#334155", fg=app.TEXT, width=20).pack(pady=5)
    tk.Button(frame, text="← Back", command=app.show_main_menu, bg=app.BG_CARD, fg=app.TEXT, width=20).pack(pady=10)