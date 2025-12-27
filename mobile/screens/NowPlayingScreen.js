import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Slider from '@react-native-community/slider';
import { colors } from '../theme';
import { usePlayer } from '../context/PlayerContext';

export default function NowPlayingScreen() {
  const { currentTrack, isPlaying, togglePlayback } = usePlayer();
  const [position, setPosition] = React.useState(0); // This would be updated by the audio player

  if (!currentTrack) {
    return (
      <View style={styles.container}>
        <Text style={styles.emptyText}>No track selected</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Album Art */}
      <View style={styles.albumArtContainer}>
        <Ionicons name="musical-notes" size={200} color={colors.textSecondary} />
      </View>

      {/* Track Info */}
      <View style={styles.trackInfoContainer}>
        <Text style={styles.trackTitle}>{currentTrack.title}</Text>
        <Text style={styles.trackArtist}>{currentTrack.artist}</Text>
      </View>

      {/* Progress Slider */}
      <View style={styles.sliderContainer}>
        <Slider
          style={styles.slider}
          minimumValue={0}
          maximumValue={currentTrack.duration || 0}
          value={position}
          minimumTrackTintColor={colors.primary}
          maximumTrackTintColor={colors.textSecondary}
          thumbTintColor={colors.primary}
        />
        <View style={styles.timeContainer}>
          <Text style={styles.timeText}>{new Date(position * 1000).toISOString().substr(14, 5)}</Text>
          <Text style={styles.timeText}>{new Date((currentTrack.duration || 0) * 1000).toISOString().substr(14, 5)}</Text>
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
  emptyText: {
    color: colors.textSecondary,
    fontSize: 18,
  },
  albumArtContainer: {
    width: 300,
    height: 300,
    backgroundColor: colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    marginBottom: 30,
  },
  trackInfoContainer: {
    alignItems: 'center',
    marginBottom: 30,
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
