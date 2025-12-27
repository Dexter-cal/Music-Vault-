from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QTabWidget, QLabel, QMenu
from PySide6.QtCore import Signal, Qt
from musicvault.view_manager import ViewManager
from musicvault.vault_manager import VaultManager

DB_PATH = "musicvault.db"

class LibraryView(QWidget):
    """A widget that displays the contents of the music library."""
    track_selected = Signal(object)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search tracks...")
        self.layout.addWidget(self.search_bar)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.all_tracks_tab = QWidget()
        self.artists_tab = QWidget()
        self.albums_tab = QWidget()
        self.recently_added_tab = QWidget()
        self.for_you_tab = QWidget()
        self.favorites_tab = QWidget()

        self.tabs.addTab(self.all_tracks_tab, "All Tracks")
        self.tabs.addTab(self.artists_tab, "Artists")
        self.tabs.addTab(self.albums_tab, "Albums")
        self.tabs.addTab(self.recently_added_tab, "Recently Added")
        self.tabs.addTab(self.favorites_tab, "Favorites")
        self.tabs.addTab(self.for_you_tab, "For You")

        # Create list widgets as member variables
        self.track_list = QListWidget()
        self.artist_list = QListWidget()
        self.album_list = QListWidget()
        self.recently_added_list = QListWidget()
        self.favorites_list = QListWidget()

        # Populate tabs
        self.setup_all_tracks_tab()
        self.setup_artists_tab()
        self.setup_albums_tab()
        self.setup_recently_added_tab()
        self.setup_favorites_tab()
        self.setup_for_you_tab()

        # Connect signals
        self.track_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        self.artist_list.itemClicked.connect(self.on_artist_selected)
        self.recently_added_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        self.favorites_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        self.search_bar.textChanged.connect(self.on_search_changed)

        # Set context menus
        self.track_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.track_list.customContextMenuRequested.connect(self.show_track_context_menu)
        self.recently_added_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.recently_added_list.customContextMenuRequested.connect(self.show_track_context_menu)
        self.favorites_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.favorites_list.customContextMenuRequested.connect(self.show_track_context_menu)

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

    def update_track_list(self, artist_name=None, album_name=None, search_query=None):
        """Updates the track list, optionally filtering by artist, album, or search query."""
        self.track_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            if search_query:
                tracks = view_manager.search_tracks(search_query)
            elif artist_name:
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

    def setup_favorites_tab(self):
        """Sets up the 'Favorites' tab with a list of favorite tracks."""
        layout = QVBoxLayout(self.favorites_tab)
        layout.addWidget(self.favorites_list)
        self.update_favorites_list()

    def update_favorites_list(self):
        """Updates the favorites list."""
        self.favorites_list.clear()
        with ViewManager(DB_PATH) as view_manager:
            tracks = view_manager.get_favorite_tracks()
            for track in tracks:
                item = QListWidgetItem(f"{track.title} - {track.artist}")
                item.setData(1, track)
                self.favorites_list.addItem(item)

    def show_track_context_menu(self, pos):
        """Shows a context menu for a track."""
        list_widget = self.sender()
        item = list_widget.itemAt(pos)
        if not item:
            return

        track = item.data(1)

        menu = QMenu()
        favorite_action = menu.addAction("Add to Favorites" if not track.is_favorite else "Remove from Favorites")
        action = menu.exec(list_widget.mapToGlobal(pos))

        if action == favorite_action:
            with VaultManager(DB_PATH) as vault_manager:
                vault_manager.toggle_favorite(track.id)
            self.update_all_views()

    def update_all_views(self):
        """Updates all the library views."""
        self.update_track_list()
        self.update_artist_list()
        self.update_album_list()
        self.update_recently_added_list()
        self.update_favorites_list()

    def on_search_changed(self, query):
        """Filters the track list based on the search query."""
        self.update_track_list(search_query=query)
        self.tabs.setCurrentWidget(self.all_tracks_tab)
