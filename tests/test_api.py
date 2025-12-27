import os
import unittest
import json
import sqlite3
from musicvault.api import create_app
from musicvault.device_manager import DeviceManager
from musicvault.view_manager import ViewManager

class ApiTestCase(unittest.TestCase):
    """Test case for the MusicVault API."""

    def setUp(self):
        """Set up a test client and initialize the database."""
        self.db_path = "test_api.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        self.app = create_app(self.db_path)
        self.client = self.app.test_client()
        self.app.testing = True

        self.device_manager = DeviceManager(self.db_path)
        self.view_manager = ViewManager(self.db_path) # For adding data

        self.add_test_data()

    def tearDown(self):
        """Clean up the database file after tests."""
        # Ensure managers are closed to release the file lock on Windows
        self.device_manager.close()
        self.view_manager.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def add_test_data(self):
        """Adds some test data to the test database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # The tables are already created by the managers, so we just add data
        cursor.execute("INSERT INTO tracks VALUES (1, 'a.mp3', 'T1', 'A1', 'Al1', 'G1', 2001, 101)")
        cursor.execute("INSERT INTO tracks VALUES (2, 'b.mp3', 'T2', 'A1', 'Al1', 'G2', 2001, 102)")
        cursor.execute("INSERT INTO tracks VALUES (3, 'c.mp3', 'T3', 'A2', 'Al2', 'G1', 2002, 103)")
        conn.commit()
        conn.close()

    def test_pair_device(self):
        """Test the device pairing endpoint."""
        response = self.client.post('/pair', json={'device_name': 'Test Phone'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('qr_code_url', data)

    def test_token_required_no_token(self):
        """Test that a protected endpoint fails without a token."""
        response = self.client.get('/library/artists')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Token is missing.')

    def test_token_required_invalid_token(self):
        """Test that a protected endpoint fails with an invalid token."""
        response = self.client.get('/library/artists', headers={'Authorization': 'Bearer invalid'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Token is invalid or expired.')

    def test_get_artists(self):
        """Test the /library/artists endpoint."""
        token = self.device_manager.pair_device('Test Phone')
        response = self.client.get('/library/artists', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(sorted(data), ['A1', 'A2'])

    def test_get_albums(self):
        """Test the /library/albums endpoint."""
        token = self.device_manager.pair_device('Test Phone')
        response = self.client.get('/library/albums', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(sorted(data), ['Al1', 'Al2'])

    def test_get_genres(self):
        """Test the /library/genres endpoint."""
        token = self.device_manager.pair_device('Test Phone')
        response = self.client.get('/library/genres', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(sorted(data), ['G1', 'G2'])

    def test_get_all_tracks(self):
        """Test fetching all tracks from the /library/tracks endpoint."""
        token = self.device_manager.pair_device('Test Phone')
        response = self.client.get('/library/tracks', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

if __name__ == '__main__':
    unittest.main()
