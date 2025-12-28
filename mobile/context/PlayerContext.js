import React, { createContext, useState, useContext, useEffect } from 'react';
import { Audio } from 'expo-av';
import apiClient from '../services/api';

const PlayerContext = createContext();

export const PlayerProvider = ({ children }) => {
  const [sound, setSound] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackStatus, setPlaybackStatus] = useState(null);

  useEffect(() => {
    Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: true,
      shouldDuckAndroid: true,
      playThroughEarpieceAndroid: false,
    });
  }, []);

  const onPlaybackStatusUpdate = (status) => {
    setPlaybackStatus(status);
    if (status.isLoaded) {
      setIsPlaying(status.isPlaying);
    }
  };

  const playTrack = async (track) => {
    if (sound) {
      await sound.unloadAsync();
      setSound(null);
    }

    if (!track) {
      setCurrentTrack(null);
      return;
    }

    const streamUrl = `${apiClient.defaults.baseURL}/stream/${track.id}`;
    const headers = { ...apiClient.defaults.headers.common };

    try {
      const { sound: newSound } = await Audio.Sound.createAsync(
        { uri: streamUrl, headers },
        { shouldPlay: true },
        onPlaybackStatusUpdate
      );
      setSound(newSound);
      setCurrentTrack(track);
    } catch (error) {
      console.error("Failed to load sound:", error);
    }
  };

  const togglePlayback = async () => {
    if (!sound) return;
    if (isPlaying) {
      await sound.pauseAsync();
    } else {
      await sound.playAsync();
    }
  };

  return (
    <PlayerContext.Provider value={{ currentTrack, isPlaying, playbackStatus, playTrack, togglePlayback }}>
      {children}
    </PlayerContext.Provider>
  );
};

export const usePlayer = () => useContext(PlayerContext);
