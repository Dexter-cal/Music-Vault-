import sqlite3
from typing import Optional, List

from musicvault.models import Playlist, SandboxItem, Track

class SandboxManager:
    """Manages the user's sandbox, including playlists and collections."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """Creates the necessary database tables for the sandbox if they don't already exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                playlist_id INTEGER,
                track_id INTEGER,
                FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                FOREIGN KEY (track_id) REFERENCES tracks(id),
                PRIMARY KEY (playlist_id, track_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sandbox_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                item_type TEXT NOT NULL,
                item_id INTEGER,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES sandbox_items(id)
            )
        ''')
        self.conn.commit()

    def create_playlist(self, name: str) -> Playlist:
        """Creates a new playlist in the database."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
        self.conn.commit()
        playlist_id = cursor.lastrowid
        return Playlist(id=playlist_id, name=name)

    def add_track_to_playlist(self, playlist_id: int, track_id: int):
        """Adds a track from the vault to a playlist."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO playlist_tracks (playlist_id, track_id) VALUES (?, ?)", (playlist_id, track_id))
        self.conn.commit()

    def get_playlist(self, playlist_id: int) -> Optional[Playlist]:
        """Retrieves a playlist and its tracks from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM playlists WHERE id=?", (playlist_id,))
        playlist_row = cursor.fetchone()

        if not playlist_row:
            return None

        playlist = Playlist(id=playlist_row[0], name=playlist_row[1])

        cursor.execute("""
            SELECT t.id, t.filepath, t.title, t.artist, t.album, t.genre, t.release_year, t.duration
            FROM tracks t
            JOIN playlist_tracks pt ON t.id = pt.track_id
            WHERE pt.playlist_id = ?
        """, (playlist_id,))

        track_rows = cursor.fetchall()
        for row in track_rows:
            playlist.tracks.append(Track(*row))

        return playlist

    def close(self):
        """Closes the database connection."""
        self.conn.close()
