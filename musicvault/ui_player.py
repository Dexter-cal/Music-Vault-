from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from musicvault.player import Player

class PlayerControls(QWidget):
    """A widget that provides playback controls for the music player."""
    def __init__(self, player: Player):
        super().__init__()
        self.player = player

        self.layout = QHBoxLayout(self)

        # Create controls
        self.play_pause_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.current_track_label = QLabel("No track selected")

        # Add controls to layout
        self.layout.addWidget(self.current_track_label)
        self.layout.addWidget(self.play_pause_button)
        self.layout.addWidget(self.stop_button)

        # Connect signals
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.player.stop)

    def toggle_play_pause(self):
        """Toggles between playing and pausing the current track."""
        if self.player.is_playing:
            self.player.pause()
            self.play_pause_button.setText("Play")
        else:
            self.player.play()
            self.play_pause_button.setText("Pause")

    def set_current_track_label(self, text: str):
        """Sets the text of the current track label."""
        self.current_track_label.setText(text)
