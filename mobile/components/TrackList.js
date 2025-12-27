import React, { useState, useEffect } from 'react';
import { FlatList, Text, StyleSheet, ActivityIndicator, View, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import apiClient from '../services/api';
import { colors } from '../theme';
import { useAuth } from '../context/AuthContext';
import { usePlayer } from '../context/PlayerContext';

export default function TrackList() {
  const { isConnected } = useAuth();
  const { playTrack } = usePlayer();
  const navigation = useNavigation();
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTracks = async () => {
      if (isConnected) {
        setLoading(true);
        try {
          const response = await apiClient.get('/library/tracks');
          setTracks(response.data);
        } catch (error) {
          console.error("Failed to fetch tracks:", error);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchTracks();
  }, [isConnected]);

  const handleTrackPress = (track) => {
    playTrack(track);
    navigation.navigate('Now Playing');
  };

  if (loading) {
    return <ActivityIndicator size="large" color={colors.primary} />;
  }

  return (
    <FlatList
      data={tracks}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <TouchableOpacity onPress={() => handleTrackPress(item)}>
          <View style={styles.itemContainer}>
            <Text style={styles.itemTitle}>{item.title}</Text>
            <Text style={styles.itemArtist}>{item.artist}</Text>
          </View>
        </TouchableOpacity>
      )}
    />
  );
}

const styles = StyleSheet.create({
  itemContainer: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  itemTitle: {
    fontSize: 16,
    color: colors.text,
  },
  itemArtist: {
    fontSize: 14,
    color: colors.textSecondary,
  },
});
