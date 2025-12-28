import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon
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
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setGeometry(100, 100, 1024, 768)

        # Create a central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create player
        self.player = Player()

        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        main_layout.addWidget(self.content_area, 1)

        # Add the library view to the content area
        self.library_view = LibraryView()
        self.content_layout.addWidget(self.library_view)

        # Connect signals
        self.library_view.track_selected.connect(self.play_track)

        # Connect sidebar buttons to the library view
        self.sidebar.findChild(QPushButton, "All Tracks").clicked.connect(
            lambda: self.library_view.update_view("all_tracks")
        )
        self.sidebar.findChild(QPushButton, "Artists").clicked.connect(
            lambda: self.library_view.update_view("artists")
        )
        self.sidebar.findChild(QPushButton, "Albums").clicked.connect(
            lambda: self.library_view.update_view("albums")
        )
        self.sidebar.findChild(QPushButton, "Recently Added").clicked.connect(
            lambda: self.library_view.update_view("recently_added")
        )
        self.sidebar.findChild(QPushButton, "Favorites").clicked.connect(
            lambda: self.library_view.update_view("favorites")
        )

        # Connect settings button
        self.sidebar.findChild(QPushButton, "Settings").clicked.connect(self.open_settings)

        # Do not start the server if we are just taking a screenshot
        if '--screenshot' not in sys.argv:
            self.api_app = create_api_server()
            self.server_thread = ServerThread(self.api_app)
            self.server_thread.daemon = True
            self.server_thread.start()

    def create_sidebar(self):
        """Creates the navigation sidebar."""
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #222222;")

        # Add navigation buttons
        buttons_data = [
            ("All Tracks", "icons/music-1.svg"),
            ("Artists", "icons/user.svg"),
            ("Albums", "icons/album.svg"),
            ("Recently Added", "icons/clock.svg"),
            ("Favorites", "icons/star.svg"),
            ("For You", "icons/magic-wand.svg"),
        ]

        for name, icon_path in buttons_data:
            btn = QPushButton(name)
            btn.setObjectName(name)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Add player controls
        self.player_controls = PlayerControls(self.player)
        sidebar_layout.addWidget(self.player_controls)

        # Add settings button
        btn_settings = QPushButton("Settings")
        btn_settings.setObjectName("Settings")
        btn_settings.setIcon(QIcon("icons/settings.svg"))
        btn_settings.setIconSize(QSize(24, 24))
        sidebar_layout.addWidget(btn_settings)

        return sidebar

    def play_track(self, track):
        """Adds a track to the queue and plays it."""
        self.player.load_track(track)
        self.player.play()
        self.player_controls.set_current_track_label(f"Now Playing: {track.title}")
        self.player_controls.play_pause_button.setIcon(self.player_controls.pause_icon)
        self.player_controls.timer.start()

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

    # Load and apply the stylesheet
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()

    if '--screenshot' in sys.argv:
        window.show()
        def take_screenshot_and_exit():
            pixmap = window.grab()
            pixmap.save("verification.png")
            print("Screenshot saved to verification.png")
            app.quit()
        QTimer.singleShot(1000, take_screenshot_and_exit)
    else:
        window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
