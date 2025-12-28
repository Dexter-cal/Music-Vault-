import sqlite3
from typing import List

from musicvault.models import Track

class ViewManager:
    """Provides different views to explore the music library."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def _execute_query(self, query: str, params: tuple = ()) -> List[Track]:
        """Executes a query and returns a list of Track objects."""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        tracks = []
        for row in rows:
            tracks.append(Track(*row))
        return tracks

    def get_all_tracks(self) -> List[Track]:
        """Returns all tracks from the library."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration FROM tracks ORDER BY artist, album, title"
        return self._execute_query(query)

    def get_tracks_by_artist(self, artist: str) -> List[Track]:
        """Returns all tracks by a specific artist."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration FROM tracks WHERE artist=? ORDER BY album, title"
        return self._execute_query(query, (artist,))

    def get_tracks_by_album(self, album: str) -> List[Track]:
        """Returns all tracks from a specific album."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration FROM tracks WHERE album=? ORDER BY title"
        return self._execute_query(query, (album,))

    def get_tracks_by_genre(self, genre: str) -> List[Track]:
        """Returns all tracks of a specific genre."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration FROM tracks WHERE genre=? ORDER BY artist, album, title"
        return self._execute_query(query, (genre,))

    def get_distinct_artists(self) -> List[str]:
        """Returns a list of all unique artists."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT artist FROM tracks ORDER BY artist")
        return [row[0] for row in cursor.fetchall()]

    def get_distinct_albums(self) -> List[str]:
        """Returns a list of all unique album titles."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT album FROM tracks ORDER BY album")
        return [row[0] for row in cursor.fetchall()]

    def get_distinct_genres(self) -> List[str]:
        """Returns a list of all unique genres."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT genre FROM tracks WHERE genre IS NOT NULL ORDER BY genre")
        return [row[0] for row in cursor.fetchall()]

    def get_track_by_id(self, track_id: int) -> List[Track]:
        """Returns a single track by its ID."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration FROM tracks WHERE id=?"
        return self._execute_query(query, (track_id,))

    def close(self):
        """Closes the database connection."""
        self.conn.close()
