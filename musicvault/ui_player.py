from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, QTimer
from musicvault.player import Player

class PlayerControls(QWidget):
    """A widget that provides playback controls for the music player."""
    def __init__(self, player: Player):
        super().__init__()
        self.player = player

        self.layout = QVBoxLayout(self)

        # Create track info and seek bar
        self.track_info_layout = QHBoxLayout()
        self.current_track_label = QLabel("No track selected")
        self.time_label = QLabel("00:00 / 00:00")
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)

        self.track_info_layout.addWidget(self.current_track_label)
        self.track_info_layout.addStretch()
        self.track_info_layout.addWidget(self.time_label)

        self.layout.addLayout(self.track_info_layout)
        self.layout.addWidget(self.seek_slider)

        # Create controls
        self.controls_layout = QHBoxLayout()
        self.play_pause_button = QPushButton()
        self.play_icon = QIcon("icons/play.svg")
        self.pause_icon = QIcon("icons/pause.svg")
        self.play_pause_button.setIcon(self.play_icon)
        self.play_pause_button.setIconSize(QSize(24, 24))

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("icons/stop.svg"))
        self.stop_button.setIconSize(QSize(24, 24))

        self.controls_layout.addStretch()
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("icons/previous.svg")) # Assuming you have a 'previous.svg'
        self.prev_button.setIconSize(QSize(24, 24))

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("icons/next.svg")) # Assuming you have a 'next.svg'
        self.next_button.setIconSize(QSize(24, 24))

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.player.get_volume() * 100)

        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.prev_button)
        self.controls_layout.addWidget(self.play_pause_button)
        self.controls_layout.addWidget(self.next_button)
        self.controls_layout.addWidget(self.stop_button)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(QLabel("Volume:"))
        self.controls_layout.addWidget(self.volume_slider)

        self.layout.addLayout(self.controls_layout)

        # Connect signals
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.stop_playback)
        self.prev_button.clicked.connect(self.player.prev_track)
        self.next_button.clicked.connect(self.player.next_track)
        self.seek_slider.sliderMoved.connect(self.player.set_position)
        self.volume_slider.valueChanged.connect(lambda value: self.player.set_volume(value / 100.0))

        # Timer for updating seek bar
        self.timer = QTimer(self)
        self.timer.setInterval(1000) # Update every second
        self.timer.timeout.connect(self.update_seek_slider)

    def toggle_play_pause(self):
        """Toggles between playing and pausing the current track."""
        if self.player.is_playing:
            self.player.pause()
            self.play_pause_button.setIcon(self.play_icon)
            self.timer.stop()
        else:
            self.player.play()
            self.play_pause_button.setIcon(self.pause_icon)
            self.timer.start()

    def stop_playback(self):
        """Stops playback and resets the UI."""
        self.player.stop()
        self.play_pause_button.setIcon(self.play_icon)
        self.timer.stop()
        self.seek_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")

    def set_current_track_label(self, text: str):
        """Sets the text of the current track label."""
        self.current_track_label.setText(text)
        duration = self.player.get_duration()
        self.seek_slider.setRange(0, int(duration))
        self.update_time_label(0, duration)

    def update_seek_slider(self):
        """Updates the seek slider's position."""
        position = self.player.get_position()
        self.seek_slider.setValue(int(position))
        self.update_time_label(position, self.player.get_duration())

    def update_time_label(self, position, duration):
        """Updates the time label."""
        pos_minutes = int(position // 60)
        pos_seconds = int(position % 60)
        dur_minutes = int(duration // 60)
        dur_seconds = int(duration % 60)
        self.time_label.setText(f"{pos_minutes:02d}:{pos_seconds:02d} / {dur_minutes:02d}:{dur_seconds:02d}")
