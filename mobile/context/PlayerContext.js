import React, { createContext, useState, useContext, useEffect } from 'react';
import { Audio } from 'expo-av';
import apiClient from '../services/api';

const PlayerContext = createContext();

export const PlayerProvider = ({ children }) => {
  const [sound, setSound] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackStatus, setPlaybackStatus] = useState(null);
  const [queue, setQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [isShuffle, setIsShuffle] = useState(false);
  const [repeatMode, setRepeatMode] = useState('off'); // 'off', 'one', 'all'

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
      if (status.didJustFinish) {
        playNext();
      }
    }
  };

  const playTrack = async (track, trackQueue = [], index = 0) => {
    if (sound) {
      await sound.unloadAsync();
    }

    if (!track) {
      setCurrentTrack(null);
      setSound(null);
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
      setQueue(trackQueue);
      setCurrentIndex(index);
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

  const seek = async (millis) => {
    if (sound) {
      await sound.setPositionAsync(millis);
    }
  };

  const playNext = () => {
    if (queue.length === 0) return;

    if (repeatMode === 'one') {
      playTrack(currentTrack, queue, currentIndex);
      return;
    }

    let nextIndex;
    if (isShuffle) {
      nextIndex = Math.floor(Math.random() * queue.length);
    } else {
      nextIndex = currentIndex + 1;
    }

    if (nextIndex >= queue.length) {
      if (repeatMode === 'all') {
        nextIndex = 0;
      } else {
        playTrack(null); // Stop playback
        return;
      }
    }
    playTrack(queue[nextIndex], queue, nextIndex);
  };

  const playPrevious = () => {
    if (queue.length === 0 || currentIndex === 0) return;
    const prevIndex = currentIndex - 1;
    playTrack(queue[prevIndex], queue, prevIndex);
  };

  const toggleShuffle = () => setIsShuffle(!isShuffle);
  const cycleRepeatMode = () => {
    const modes = ['off', 'all', 'one'];
    const nextIndex = (modes.indexOf(repeatMode) + 1) % modes.length;
    setRepeatMode(modes[nextIndex]);
  };

  return (
    <PlayerContext.Provider value={{
      currentTrack, isPlaying, playbackStatus, playTrack, togglePlayback, seek,
      playNext, playPrevious, isShuffle, toggleShuffle, repeatMode, cycleRepeatMode,
    }}>
      {children}
    </PlayerContext.Provider>
  );
};

export const usePlayer = () => useContext(PlayerContext);
