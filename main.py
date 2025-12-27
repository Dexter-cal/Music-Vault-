import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer
from musicvault.api_server import create_api_server, ServerThread
from musicvault.vault_manager import VaultManager
from musicvault.sandbox_manager import SandboxManager
from musicvault.ui_library import LibraryView
from musicvault.ui_player import PlayerControls
from musicvault.player import Player
from musicvault.ui_settings import SettingsWindow

DB_PATH = "musicvault.db"

class MainWindow(QMainWindow):
    """The main window for the MusicVault desktop application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MusicVault")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the player
        self.player = Player()

        # Add the library view
        self.library_view = LibraryView()
        layout.addWidget(self.library_view)

        # Add the player controls
        self.player_controls = PlayerControls(self.player)
        layout.addWidget(self.player_controls)

        # Add settings button
        self.settings_button = QPushButton("Settings")
        layout.addWidget(self.settings_button)
        self.settings_button.clicked.connect(self.open_settings)

        # Connect signals
        self.library_view.track_selected.connect(self.play_track)

        # Do not start the server if we are just taking a screenshot
        if '--screenshot' not in sys.argv:
            self.api_app = create_api_server()
            self.server_thread = ServerThread(self.api_app)
            self.server_thread.daemon = True
            self.server_thread.start()

    def play_track(self, track):
        """Loads and plays the selected track."""
        self.player.load_track(track.filepath)
        self.player.play()
        self.player_controls.set_current_track_label(f"Now Playing: {track.title}")
        self.player_controls.play_pause_button.setText("Pause")

    def open_settings(self):
        """Opens the settings window."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()

def main():
    """The main entry point for the application."""
    if '--screenshot' in sys.argv:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"

    # Ensure the database and tables are created before starting the app
    vault_manager = VaultManager(DB_PATH)
    sandbox_manager = SandboxManager(DB_PATH)
    vault_manager.close()
    sandbox_manager.close()

    app = QApplication(sys.argv)
    window = MainWindow()

    if '--screenshot' in sys.argv:
        # In screenshot mode, show the window, take a screenshot after a delay, and exit.
        window.show()
        def take_screenshot_and_exit():
            pixmap = window.grab()
            pixmap.save("verification.png")
            print("Screenshot saved to verification.png")
            app.quit()
        QTimer.singleShot(1000, take_screenshot_and_exit) # 1 second delay for rendering
    else:
        # In normal mode, just show the window.
        window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
