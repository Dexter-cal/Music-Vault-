import json
import os

SETTINGS_FILE = "settings.json"

def save_setting(key, value):
    """Saves a key-value pair to the settings file."""
    settings = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                pass  # Ignore corrupted or empty file

    settings[key] = value

    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_setting(key, default=None):
    """Loads a value for a given key from the settings file."""
    if not os.path.exists(SETTINGS_FILE):
        return default

    with open(SETTINGS_FILE, 'r') as f:
        try:
            settings = json.load(f)
            return settings.get(key, default)
        except json.JSONDecodeError:
            return default # Return default if file is corrupted
