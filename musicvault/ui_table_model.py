from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Any
from musicvault.models import Track

class TrackTableModel(QAbstractTableModel):
    """A table model for displaying a list of Track objects."""

    def __init__(self, tracks: List[Track]):
        super().__init__()
        self._tracks = tracks
        self._headers = ["Title", "Artist", "Album", "Genre", "Year", "Duration", "Favorite"]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Returns the number of rows in the model."""
        return len(self._tracks)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Returns the number of columns in the model."""
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Returns the data for the given index and role."""
        if not index.isValid():
            return None

        track = self._tracks[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return track.title
            elif column == 1:
                return track.artist
            elif column == 2:
                return track.album
            elif column == 3:
                return track.genre
            elif column == 4:
                return track.release_year
            elif column == 5:
                # Format duration as MM:SS
                if track.duration:
                    minutes = int(track.duration // 60)
                    seconds = int(track.duration % 60)
                    return f"{minutes:02d}:{seconds:02d}"
                return "N/A"
            elif column == 6:
                return "★" if track.is_favorite else ""

        elif role == Qt.ItemDataRole.UserRole:
            return track

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Returns the header data for the given section, orientation, and role."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        """Sorts the model by the given column and order."""
        self.layoutAboutToBeChanged.emit()
        reverse = order == Qt.SortOrder.DescendingOrder

        key = None
        if column == 0:
            key = lambda t: t.title or ""
        elif column == 1:
            key = lambda t: t.artist or ""
        elif column == 2:
            key = lambda t: t.album or ""
        elif column == 3:
            key = lambda t: t.genre or ""
        elif column == 4:
            key = lambda t: t.release_year or 0
        elif column == 5:
            key = lambda t: t.duration or 0
        elif column == 6:
            key = lambda t: t.is_favorite

        if key:
            self._tracks.sort(key=key, reverse=reverse)

        self.layoutChanged.emit()
