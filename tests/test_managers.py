import unittest
import os
import subprocess
import sqlite3
from unittest.mock import patch
from mutagen.easyid3 import EasyID3

from musicvault.vault_manager import VaultManager
from musicvault.sandbox_manager import SandboxManager
from musicvault.view_manager import ViewManager
from musicvault.models import Track
import time

class TestSandboxAndViewManagers(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database and managers for testing."""
        self.db_path = "test_managers.db"

        # Patch the fingerprint generator to return unique fingerprints
        self.fingerprint_patcher = patch('musicvault.vault_manager.VaultManager._generate_fingerprint')
        self.mock_fingerprint = self.fingerprint_patcher.start()

        self.fingerprint_counter = 0
        def unique_fingerprint_side_effect(filepath):
            self.fingerprint_counter += 1
            return f"unique_fingerprint_{self.fingerprint_counter}"
        self.mock_fingerprint.side_effect = unique_fingerprint_side_effect

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
        self.fingerprint_patcher.stop()
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

    def test_get_recently_added_tracks(self):
        """Test retrieving recently added tracks."""
        # Add a second track after a short delay
        time.sleep(1)
        dummy_filepath2 = "dummy_test2.mp3"
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
            '-t', '1', '-q:a', '9', '-acodec', 'libmp3lame', dummy_filepath2
        ], check=True, capture_output=True)
        audio = EasyID3()
        audio['title'] = 'Test Song 2'
        audio['artist'] = 'Test Artist 2'
        audio.save(dummy_filepath2)
        track2 = self.vault_manager.add_track(dummy_filepath2)

        recently_added = self.view_manager.get_recently_added_tracks(limit=2)
        self.assertEqual(len(recently_added), 2)
        self.assertEqual(recently_added[0].title, "Test Song 2")
        self.assertEqual(recently_added[1].title, "Test Song")

        os.remove(dummy_filepath2)

    def test_search_tracks(self):
        """Test searching for tracks."""
        # Add a second track
        dummy_filepath2 = "dummy_test2.mp3"
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
            '-t', '1', '-q:a', '9', '-acodec', 'libmp3lame', dummy_filepath2
        ], check=True, capture_output=True)
        audio = EasyID3()
        audio['title'] = 'Another Song'
        audio['artist'] = 'Another Artist'
        audio.save(dummy_filepath2)
        self.vault_manager.add_track(dummy_filepath2)

        # Search by title
        results = self.view_manager.search_tracks("Another Song")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Another Song")

        # Search by artist
        results = self.view_manager.search_tracks("Another Artist")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].artist, "Another Artist")

        os.remove(dummy_filepath2)

    def test_favorites(self):
        """Test toggling favorite status and retrieving favorite tracks."""
        # Mark track as favorite
        self.vault_manager.toggle_favorite(self.test_track.id)

        # Verify it's in favorites
        favorites = self.view_manager.get_favorite_tracks()
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0].title, "Test Song")

        # Unmark as favorite
        self.vault_manager.toggle_favorite(self.test_track.id)

        # Verify it's not in favorites
        favorites = self.view_manager.get_favorite_tracks()
        self.assertEqual(len(favorites), 0)

if __name__ == '__main__':
    unittest.main()
