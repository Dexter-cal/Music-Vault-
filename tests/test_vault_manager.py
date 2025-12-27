import unittest
import os
import sqlite3
import subprocess
from mutagen.easyid3 import EasyID3
from musicvault.vault_manager import VaultManager
from musicvault.models import Track

class TestVaultManager(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database and a dummy mp3 file for testing."""
        self.db_path = "test.db"
        self.vault_manager = VaultManager(self.db_path)

        # Create a dummy MP3 file using ffmpeg.
        self.dummy_filepath = "dummy.mp3"
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
            '-t', '1', '-q:a', '9', '-acodec', 'libmp3lame', self.dummy_filepath
        ], check=True, capture_output=True)

        audio = EasyID3()
        audio['title'] = 'Test Title'
        audio['artist'] = 'Test Artist'
        audio['album'] = 'Test Album'
        audio['genre'] = 'Test Genre'
        audio['date'] = '2023'
        audio.save(self.dummy_filepath)


    def tearDown(self):
        """Clean up the temporary database and dummy file."""
        self.vault_manager.close()
        os.remove(self.db_path)
        os.remove(self.dummy_filepath)

    def test_add_track(self):
        """Test adding a track to the vault."""
        track = self.vault_manager.add_track(self.dummy_filepath)
        self.assertIsNotNone(track)
        self.assertEqual(track.title, 'Test Title')
        self.assertEqual(track.artist, 'Test Artist')
        self.assertEqual(track.album, 'Test Album')
        self.assertEqual(track.genre, 'Test Genre')
        self.assertEqual(track.release_year, 2023)

        # Verify that the track is in the database
        cursor = self.vault_manager.conn.cursor()
        cursor.execute("SELECT * FROM tracks WHERE filepath=?", (self.dummy_filepath,))
        db_track = cursor.fetchone()
        self.assertIsNotNone(db_track)
        self.assertEqual(db_track[2], 'Test Title')

    def test_add_nonexistent_track(self):
        """Test adding a track that does not exist."""
        track = self.vault_manager.add_track("nonexistent.mp3")
        self.assertIsNone(track)

if __name__ == '__main__':
    unittest.main()
