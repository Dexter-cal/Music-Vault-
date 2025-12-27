from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTableView, QAbstractItemView, QLabel, QMenu
from PySide6.QtCore import Signal, Qt
from musicvault.ui_table_model import TrackTableModel
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

        # This table will be used to display the current view
        self.track_table = QTableView()
        self.track_table.setSortingEnabled(True)
        self.track_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.track_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.track_table)

        # Connect signals
        self.track_table.doubleClicked.connect(self.on_track_double_clicked)
        self.search_bar.textChanged.connect(self.on_search_changed)

        # Set context menu
        self.track_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.track_table.customContextMenuRequested.connect(self.show_track_context_menu)

        # Initial view
        self.update_view("all_tracks")

    def update_view(self, view_type, filter_term=None):
        """Updates the library view based on the selected view type."""
        with ViewManager(DB_PATH) as view_manager:
            tracks = []
            if view_type == "all_tracks":
                tracks = view_manager.get_all_tracks()
            elif view_type == "artists":
                # For now, we will just show all tracks for artists view
                tracks = view_manager.get_all_tracks()
            elif view_type == "albums":
                 # For now, we will just show all tracks for albums view
                tracks = view_manager.get_all_tracks()
            elif view_type == "recently_added":
                tracks = view_manager.get_recently_added_tracks()
            elif view_type == "favorites":
                tracks = view_manager.get_favorite_tracks()
            elif view_type == "search":
                tracks = view_manager.search_tracks(filter_term)

            self.model = TrackTableModel(tracks)
            self.track_table.setModel(self.model)

    def show_track_context_menu(self, pos):
        """Shows a context menu for a track."""
        index = self.track_table.indexAt(pos)
        if not index.isValid():
            return

        track = self.model.data(index, Qt.ItemDataRole.UserRole)

        menu = QMenu()
        favorite_action = menu.addAction("Add to Favorites" if not track.is_favorite else "Remove from Favorites")
        action = menu.exec(self.track_table.viewport().mapToGlobal(pos))

        if action == favorite_action:
            with VaultManager(DB_PATH) as vault_manager:
                vault_manager.toggle_favorite(track.id)
            self.update_view("all_tracks") # Refresh the view

    def on_search_changed(self, query):
        """Filters the track list based on the search query."""
        self.update_view("search", filter_term=query)

    def on_track_double_clicked(self, index):
        """Emits the track_selected signal when a track is double-clicked."""
        track = self.model.data(index, Qt.ItemDataRole.UserRole)
        self.track_selected.emit(track)
