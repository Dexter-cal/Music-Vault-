from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QTabWidget
from PySide6.QtCore import Signal
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

        self.tabs.addTab(self.all_tracks_tab, "All Tracks")
        self.tabs.addTab(self.artists_tab, "Artists")
        self.tabs.addTab(self.albums_tab, "Albums")

        # Populate tabs
        self.setup_all_tracks_tab()
        self.setup_artists_tab()
        self.setup_albums_tab()

    def setup_all_tracks_tab(self):
        """Sets up the 'All Tracks' tab with a list of all tracks."""
        layout = QVBoxLayout(self.all_tracks_tab)
        track_list = QListWidget()
        track_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        layout.addWidget(track_list)

        with ViewManager(DB_PATH) as view_manager:
            tracks = view_manager.get_all_tracks()
            for track in tracks:
                item = QListWidgetItem(f"{track.title} - {track.artist}")
                item.setData(1, track) # Store the track object with the item
                track_list.addItem(item)

    def setup_artists_tab(self):
        """Sets up the 'Artists' tab with a list of all artists."""
        layout = QVBoxLayout(self.artists_tab)
        artist_list = QListWidget()
        layout.addWidget(artist_list)

        with ViewManager(DB_PATH) as view_manager:
            artists = view_manager.get_distinct_artists()
            for artist in artists:
                item = QListWidgetItem(artist)
                artist_list.addItem(item)

    def setup_albums_tab(self):
        """Sets up the 'Albums' tab with a list of all albums."""
        layout = QVBoxLayout(self.albums_tab)
        album_list = QListWidget()
        layout.addWidget(album_list)

        with ViewManager(DB_PATH) as view_manager:
            albums = view_manager.get_distinct_albums()
            for album in albums:
                item = QListWidgetItem(album)
                album_list.addItem(item)

    def on_track_double_clicked(self, item):
        """Emits the track_selected signal when a track is double-clicked."""
        track = item.data(1)
        self.track_selected.emit(track)
