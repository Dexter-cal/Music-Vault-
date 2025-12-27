from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QTabWidget, QLabel
from PySide6.QtCore import Signal, Qt
from musicvault.view_manager import ViewManager

DB_PATH = "musicvault.db"

class LibraryView(QWidget):
    """A widget that displays the contents of the music library."""
    track_selected = Signal(object)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.all_tracks_tab = QWidget()
        self.artists_tab = QWidget()
        self.albums_tab = QWidget()
        self.recently_added_tab = QWidget()
        self.for_you_tab = QWidget()

        self.tabs.addTab(self.all_tracks_tab, "All Tracks")
        self.tabs.addTab(self.artists_tab, "Artists")
        self.tabs.addTab(self.albums_tab, "Albums")
        self.tabs.addTab(self.recently_added_tab, "Recently Added")
        self.tabs.addTab(self.for_you_tab, "For You")

        # Create list widgets as member variables
        self.track_list = QListWidget()
        self.artist_list = QListWidget()
        self.album_list = QListWidget()
        self.recently_added_list = QListWidget()

        # Populate tabs
        self.setup_all_tracks_tab()
        self.setup_artists_tab()
        self.setup_albums_tab()
        self.setup_recently_added_tab()
        self.setup_for_you_tab()

        # Connect signals
        self.track_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        self.artist_list.itemClicked.connect(self.on_artist_selected)
        self.recently_added_list.itemDoubleClicked.connect(self.on_track_double_clicked)

    def setup_all_tracks_tab(self):
        """Sets up the 'All Tracks' tab with a list of all tracks."""
        layout = QVBoxLayout(self.all_tracks_tab)
        layout.addWidget(self.track_list)
        self.update_track_list() # Initial population

    def setup_artists_tab(self):
        """Sets up the 'Artists' tab with a list of all artists."""
        layout = QVBoxLayout(self.artists_tab)
        layout.addWidget(self.artist_list)
        self.update_artist_list()

    def setup_albums_tab(self):
        """Sets up the 'Albums' tab with a list of all albums."""
        layout = QVBoxLayout(self.albums_tab)
        layout.addWidget(self.album_list)
        self.update_album_list()

    def update_track_list(self, artist_name=None, album_name=None):
        """Updates the track list, optionally filtering by artist or album."""
        self.track_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            if artist_name:
                tracks = view_manager.get_tracks_by_artist(artist_name)
            elif album_name:
                tracks = view_manager.get_tracks_by_album(album_name)
            else:
                tracks = view_manager.get_all_tracks()

            for track in tracks:
                item = QListWidgetItem(f"{track.title} - {track.artist}")
                item.setData(1, track)
                self.track_list.addItem(item)

    def update_artist_list(self):
        """Updates the artist list."""
        self.artist_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            artists = view_manager.get_distinct_artists()
            for artist in artists:
                self.artist_list.addItem(QListWidgetItem(artist))

    def update_album_list(self):
        """Updates the album list."""
        self.album_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            albums = view_manager.get_distinct_albums()
            for album in albums:
                self.album_list.addItem(QListWidgetItem(album))

    def on_artist_selected(self, item):
        """Filters the track list when an artist is selected."""
        artist_name = item.text()
        self.update_track_list(artist_name=artist_name)
        self.tabs.setCurrentWidget(self.all_tracks_tab)

    def setup_recently_added_tab(self):
        """Sets up the 'Recently Added' tab with a list of the latest tracks."""
        layout = QVBoxLayout(self.recently_added_tab)
        layout.addWidget(self.recently_added_list)
        self.update_recently_added_list()

    def update_recently_added_list(self):
        """Updates the recently added list."""
        self.recently_added_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            tracks = view_manager.get_recently_added_tracks()
            for track in tracks:
                item = QListWidgetItem(f"{track.title} - {track.artist}")
                item.setData(1, track)
                self.recently_added_list.addItem(item)

    def on_track_double_clicked(self, item):
        """Emits the track_selected signal when a track is double-clicked."""
        track = item.data(1)
        self.track_selected.emit(track)

    def setup_for_you_tab(self):
        """Sets up the 'For You' tab with a placeholder for AI suggestions."""
        layout = QVBoxLayout(self.for_you_tab)
        placeholder_label = QLabel("AI-powered suggestions will appear here.\nEnable AI in Settings to get started.")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder_label)
