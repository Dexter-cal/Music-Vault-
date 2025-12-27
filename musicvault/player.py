import pygame
import os

class Player:
    """Handles the audio playback logic for the application."""
    def __init__(self):
        # Use a dummy audio driver in headless environments
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            os.environ["SDL_AUDIODRIVER"] = "dummy"

        pygame.mixer.init()
        self.current_track = None
        self.is_playing = False

    def load_track(self, filepath: str):
        """Loads a track for playback."""
        if self.is_playing:
            self.stop()
        self.current_track = filepath
        pygame.mixer.music.load(self.current_track)

    def play(self):
        """Plays the currently loaded track."""
        if self.current_track:
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
        self.current_track = None
