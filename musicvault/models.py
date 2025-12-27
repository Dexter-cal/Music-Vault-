from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Track:
    """Represents a single audio track in the music library."""
    id: int
    filepath: str
    title: str
    artist: str
    album: str
    genre: Optional[str] = None
    release_year: Optional[int] = None
    duration: Optional[float] = None
    fingerprint: Optional[str] = None
    date_added: Optional[str] = None
    is_favorite: bool = False

@dataclass
class Playlist:
    """Represents a user-defined playlist of tracks."""
    id: int
    name: str
    tracks: List[Track] = field(default_factory=list)

@dataclass
class SandboxItem:
    """Represents a flexible item in the user's sandbox, which can be a track, playlist, or folder."""
    id: int
    name: str
    item_type: str  # 'track', 'playlist', or 'folder'
    item_id: Optional[int] = None  # Refers to Track.id or Playlist.id
    parent_id: Optional[int] = None
