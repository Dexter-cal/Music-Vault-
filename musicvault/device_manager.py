import sqlite3
import secrets
import pyqrcode
from io import BytesIO
from typing import Optional

class DeviceManager:
    """Manages the pairing and authentication of mobile devices."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """Creates the database table for storing trusted devices."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trusted_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT NOT NULL,
                token TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    def pair_device(self, device_name: str) -> str:
        """Generates a unique token for a new device and stores it."""
        token = secrets.token_hex(16)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO trusted_devices (device_name, token) VALUES (?, ?)", (device_name, token))
        self.conn.commit()
        return token

    def get_pairing_qrcode_in_memory(self, token: str) -> BytesIO:
        """Generates a QR code image in memory and returns it as a BytesIO buffer."""
        qr = pyqrcode.create(token)
        buffer = BytesIO()
        qr.png(buffer, scale=6)
        buffer.seek(0)
        return buffer

    def is_token_valid(self, token: str) -> bool:
        """Checks if a given token is valid and corresponds to a trusted device."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM trusted_devices WHERE token=?", (token,))
        return cursor.fetchone() is not None

    def close(self):
        """Closes the database connection."""
        self.conn.close()
