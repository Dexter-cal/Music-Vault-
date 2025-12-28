import sqlite3
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from typing import Optional
import acoustid
from musicvault.models import Track

class VaultManager:
    """Manages the music library, including adding files and querying the database."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """Creates the necessary database tables if they don't already exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL UNIQUE,
                title TEXT,
                artist TEXT,
                album TEXT,
                genre TEXT,
                release_year INTEGER,
                duration REAL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0,
                fingerprint TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def _generate_fingerprint(self, filepath: str) -> Optional[str]:
        """Generates an audio fingerprint for the given file."""
        try:
            duration, fingerprint_bytes = acoustid.fingerprint_file(filepath)
            return fingerprint_bytes.decode('utf-8')
        except Exception as e:
            print(f"Error generating fingerprint for {filepath}: {e}")
            return None

    def fingerprint_exists(self, fingerprint: str) -> bool:
        """Checks if a fingerprint already exists in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM tracks WHERE fingerprint=?", (fingerprint,))
        return cursor.fetchone() is not None

    def add_track(self, filepath: str) -> Optional[Track]:
        """
        Adds a track to the vault, extracting metadata and storing it in the database.
        Skips adding the track if a duplicate is found based on the audio fingerprint.
        """
        if not os.path.exists(filepath):
            return None

        fingerprint = self._generate_fingerprint(filepath)
        if fingerprint and self.fingerprint_exists(fingerprint):
            print(f"Duplicate track detected: {filepath}")
            return None

        try:
            audio = MP3(filepath, ID3=EasyID3)
            title = audio.get('title', ['Unknown Title'])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            album = audio.get('album', ['Unknown Album'])[0]
            genre = audio.get('genre', [None])[0]

            # Year is often stored in the 'date' tag.
            release_year_str = audio.get('date', [None])[0]
            release_year = int(release_year_str) if release_year_str and release_year_str.isdigit() else None

            duration = audio.info.length

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tracks (filepath, title, artist, album, genre, release_year, duration, fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (filepath, title, artist, album, genre, release_year, duration, fingerprint)
            )
            self.conn.commit()
            track_id = cursor.lastrowid

            # Retrieve the newly inserted track to get the date_added
            cursor.execute("SELECT date_added FROM tracks WHERE id=?", (track_id,))
            date_added = cursor.fetchone()[0]

            return Track(
                id=track_id,
                filepath=filepath,
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                release_year=release_year,
                duration=duration,
                fingerprint=fingerprint
            )
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            return None

    def toggle_favorite(self, track_id: int):
        """Toggles the favorite status of a track."""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tracks SET is_favorite = NOT is_favorite WHERE id=?", (track_id,))
        self.conn.commit()

    def close(self):
        """Closes the database connection."""
        self.conn.close()
