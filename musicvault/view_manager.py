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
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks ORDER BY artist, album, title"
        return self._execute_query(query)

    def get_tracks_by_artist(self, artist: str) -> List[Track]:
        """Returns all tracks by a specific artist."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks WHERE artist=? ORDER BY album, title"
        return self._execute_query(query, (artist,))

    def get_tracks_by_album(self, album: str) -> List[Track]:
        """Returns all tracks from a specific album."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks WHERE album=? ORDER BY title"
        return self._execute_query(query, (album,))

    def get_tracks_by_genre(self, genre: str) -> List[Track]:
        """Returns all tracks of a specific genre."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks WHERE genre=? ORDER BY artist, album, title"
        return self._execute_query(query, (genre,))

    def get_distinct_artists(self) -> List[str]:
        """Returns a list of all unique artists."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT artist FROM tracks ORDER BY artist")
        return [row[0] for row in cursor.fetchall()]

    def get_distinct_albums(self) -> List[str]:
        """Returns a list of all unique albums."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT album FROM tracks ORDER BY album")
        return [row[0] for row in cursor.fetchall()]

    def get_recently_added_tracks(self, limit: int = 20) -> List[Track]:
        """Returns the most recently added tracks."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks ORDER BY date_added DESC LIMIT ?"
        return self._execute_query(query, (limit,))

    def search_tracks(self, search_query: str) -> List[Track]:
        """Searches for tracks by title, artist, or album."""
        query = """
            SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite
            FROM tracks
            WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?
            ORDER BY artist, album, title
        """
        search_term = f"%{search_query}%"
        return self._execute_query(query, (search_term, search_term, search_term))

    def get_favorite_tracks(self) -> List[Track]:
        """Returns all favorite tracks from the library."""
        query = "SELECT id, filepath, title, artist, album, genre, release_year, duration, date_added, is_favorite FROM tracks WHERE is_favorite=1 ORDER BY artist, album, title"
        return self._execute_query(query)

    def __enter__(self):
        """Enters a context management block."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits a context management block, closing the connection."""
        self.conn.close()

    def close(self):
        """Closes the database connection."""
        self.conn.close()
