import pygame
import os
from musicvault.config import load_setting, save_setting

class Player:
    """Handles the audio playback logic for the application."""
    def __init__(self):
        # Use a dummy audio driver in headless environments
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            os.environ["SDL_AUDIODRIVER"] = "dummy"

        pygame.mixer.init()
        self.queue = []
        self.current_track_index = -1
        self.is_playing = False

        initial_volume = load_setting('player_volume', 0.5)
        pygame.mixer.music.set_volume(initial_volume)

    def load_track(self, track):
        """Loads a track for playback and adds it to the queue."""
        self.queue.append(track)
        if not self.is_playing:
            self.current_track_index = len(self.queue) - 1
            pygame.mixer.music.load(track.filepath)

    def play(self):
        """Plays the currently loaded track."""
        if self.queue:
            pygame.mixer.music.play()
            self.is_playing = True

    def pause(self):
        """Pauses the currently playing track."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop(self):
        """Stops the currently playing track."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.queue = []
        self.current_track_index = -1

    def next_track(self):
        """Plays the next track in the queue."""
        if self.current_track_index < len(self.queue) - 1:
            self.current_track_index += 1
            pygame.mixer.music.load(self.queue[self.current_track_index].filepath)
            self.play()

    def prev_track(self):
        """Plays the previous track in the queue."""
        if self.current_track_index > 0:
            self.current_track_index -= 1
            pygame.mixer.music.load(self.queue[self.current_track_index].filepath)
            self.play()

    def get_duration(self):
        """Returns the duration of the currently loaded track in seconds."""
        if self.queue:
            return pygame.mixer.Sound(self.queue[self.current_track_index].filepath).get_length()
        return 0

    def get_position(self):
        """Returns the current playback position in seconds."""
        return pygame.mixer.music.get_pos() / 1000.0

    def set_position(self, position):
        """Sets the playback position in seconds."""
        pygame.mixer.music.set_pos(position)

    def get_volume(self):
        """Gets the current volume."""
        return pygame.mixer.music.get_volume()

    def set_volume(self, volume):
        """Sets the volume."""
        pygame.mixer.music.set_volume(volume)
        save_setting('player_volume', volume)
