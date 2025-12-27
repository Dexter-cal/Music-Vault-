import unittest
import os
import subprocess
import sqlite3
from mutagen.easyid3 import EasyID3

from musicvault.vault_manager import VaultManager
from musicvault.sandbox_manager import SandboxManager
from musicvault.view_manager import ViewManager
from musicvault.models import Track

class TestSandboxAndViewManagers(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database and managers for testing."""
        self.db_path = "test_managers.db"
        self.vault_manager = VaultManager(self.db_path)
        self.sandbox_manager = SandboxManager(self.db_path)
        self.view_manager = ViewManager(self.db_path)

        # Create and add a dummy track for testing
        self.dummy_filepath = "dummy_test.mp3"
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
            '-t', '1', '-q:a', '9', '-acodec', 'libmp3lame', self.dummy_filepath
        ], check=True, capture_output=True)

        audio = EasyID3()
        audio['title'] = 'Test Song'
        audio['artist'] = 'Test Artist'
        audio['album'] = 'Test Album'
        audio['genre'] = 'Rock'
        audio['date'] = '2024'
        audio.save(self.dummy_filepath)

        self.test_track = self.vault_manager.add_track(self.dummy_filepath)
        self.assertIsNotNone(self.test_track)

    def tearDown(self):
        """Clean up the temporary database and dummy file."""
        self.vault_manager.close()
        self.sandbox_manager.close()
        self.view_manager.close()
        os.remove(self.db_path)
        os.remove(self.dummy_filepath)

    # --- SandboxManager Tests ---
    def test_create_and_get_playlist(self):
        """Test creating a playlist and then retrieving it."""
        playlist = self.sandbox_manager.create_playlist("My Rock Anthems")
        self.assertEqual(playlist.name, "My Rock Anthems")
        self.assertEqual(len(playlist.tracks), 0)

        retrieved_playlist = self.sandbox_manager.get_playlist(playlist.id)
        self.assertIsNotNone(retrieved_playlist)
        self.assertEqual(retrieved_playlist.name, "My Rock Anthems")

    def test_add_track_to_playlist(self):
        """Test adding a track to a playlist."""
        playlist = self.sandbox_manager.create_playlist("Favorites")
        self.sandbox_manager.add_track_to_playlist(playlist.id, self.test_track.id)

        retrieved_playlist = self.sandbox_manager.get_playlist(playlist.id)
        self.assertEqual(len(retrieved_playlist.tracks), 1)
        self.assertEqual(retrieved_playlist.tracks[0].title, "Test Song")

    # --- ViewManager Tests ---
    def test_get_all_tracks(self):
        """Test retrieving all tracks from the vault."""
        tracks = self.view_manager.get_all_tracks()
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].title, "Test Song")

    def test_get_tracks_by_artist(self):
        """Test retrieving tracks filtered by artist."""
        tracks = self.view_manager.get_tracks_by_artist("Test Artist")
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].artist, "Test Artist")

        tracks_none = self.view_manager.get_tracks_by_artist("Unknown Artist")
        self.assertEqual(len(tracks_none), 0)

    def test_get_distinct_artists(self):
        """Test retrieving a unique list of artists."""
        artists = self.view_manager.get_distinct_artists()
        self.assertIn("Test Artist", artists)
        self.assertEqual(len(artists), 1)

if __name__ == '__main__':
    unittest.main()
