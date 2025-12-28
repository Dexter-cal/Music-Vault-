import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Slider from '@react-native-community/slider';
import { colors } from '../theme';
import { usePlayer } from '../context/PlayerContext';

export default function NowPlayingScreen() {
  const { currentTrack, isPlaying, playbackStatus, togglePlayback } = usePlayer();

  const formatMillis = (millis) => {
    const totalSeconds = millis / 1000;
    const seconds = Math.floor(totalSeconds % 60);
    const minutes = Math.floor(totalSeconds / 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  if (!currentTrack) {
    return (
      <View style={styles.container}>
        <Image source={require('../assets/logo.png')} style={styles.logo} />
        <Text style={styles.emptyText}>No track selected</Text>
      </View>
    );
  }

  const position = playbackStatus?.positionMillis || 0;
  const duration = playbackStatus?.durationMillis || currentTrack.duration * 1000 || 0;

  return (
    <View style={styles.container}>
      {/* Album Art */}
      <View style={styles.albumArtContainer}>
        <Image source={require('../assets/logo.png')} style={styles.albumArt} />
      </View>

      {/* Track Info */}
      <View style={styles.trackInfoContainer}>
        <Text style={styles.trackTitle} numberOfLines={1}>{currentTrack.title}</Text>
        <Text style={styles.trackArtist}>{currentTrack.artist}</Text>
      </View>

      {/* Progress Slider */}
      <View style={styles.sliderContainer}>
        <Slider
          style={styles.slider}
          minimumValue={0}
          maximumValue={duration}
          value={position}
          minimumTrackTintColor={colors.primary}
          maximumTrackTintColor={colors.textSecondary}
          thumbTintColor={colors.primary}
          // onSlidingComplete={(value) => sound?.setPositionAsync(value)} // Implement seek
        />
        <View style={styles.timeContainer}>
          <Text style={styles.timeText}>{formatMillis(position)}</Text>
          <Text style={styles.timeText}>{formatMillis(duration)}</Text>
        </View>
      </View>

      {/* Controls */}
      <View style={styles.controlsContainer}>
        <TouchableOpacity>
          <Ionicons name="play-skip-back" size={40} color={colors.text} />
        </TouchableOpacity>
        <TouchableOpacity onPress={togglePlayback}>
          <Ionicons name={isPlaying ? 'pause-circle' : 'play-circle'} size={70} color={colors.text} />
        </TouchableOpacity>
        <TouchableOpacity>
          <Ionicons name="play-skip-forward" size={40} color={colors.text} />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  logo: {
    width: 150,
    height: 150,
    marginBottom: 20,
  },
  emptyText: {
    color: colors.textSecondary,
    fontSize: 18,
  },
  albumArtContainer: {
    width: 300,
    height: 300,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  albumArt: {
    width: '100%',
    height: '100%',
    borderRadius: 10,
  },
  trackInfoContainer: {
    alignItems: 'center',
    marginBottom: 30,
    width: '100%',
  },
  trackTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    textAlign: 'center',
  },
  trackArtist: {
    fontSize: 18,
    color: colors.textSecondary,
  },
  sliderContainer: {
    width: '100%',
    marginBottom: 30,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  timeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
  },
  timeText: {
    color: colors.textSecondary,
  },
  controlsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    width: '80%',
  },
});
