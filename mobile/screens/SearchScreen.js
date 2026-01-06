import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, TextInput, FlatList, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import debounce from 'lodash.debounce';
import apiClient from '../services/api';
import { colors } from '../theme';
import { usePlayer } from '../context/PlayerContext';

export default function SearchScreen() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const { playTrack } = usePlayer();
  const navigation = useNavigation();

  const handleSearch = async (text) => {
    setQuery(text);
    if (text.length > 2) {
      try {
        const response = await apiClient.get(`/search?q=${text}`);
        setResults(response.data);
      } catch (error) {
        console.error("Failed to fetch search results:", error);
      }
    } else {
      setResults(null);
    }
  };

  const debouncedSearch = useCallback(debounce(handleSearch, 300), []);

  const handleTrackPress = (track) => {
    playTrack(track, [track], 0);
    navigation.navigate('Now Playing');
  };

  const renderItem = ({ item }) => {
    if (item.type === 'header') {
      return <Text style={styles.header}>{item.title}</Text>;
    }
    if (item.type === 'track') {
      return (
        <TouchableOpacity onPress={() => handleTrackPress(item.data)}>
          <View style={styles.itemContainer}>
            <Text style={styles.itemTitle}>{item.data.title}</Text>
            <Text style={styles.itemArtist}>{item.data.artist}</Text>
          </View>
        </TouchableOpacity>
      );
    }
    return (
      <View style={styles.itemContainer}>
        <Text style={styles.itemTitle}>{item.data}</Text>
      </View>
    );
  };

  const data = [];
  if (results) {
    if (results.tracks.length > 0) {
      data.push({ type: 'header', title: 'Songs' });
      results.tracks.forEach(track => data.push({ type: 'track', data: track }));
    }
    if (results.artists.length > 0) {
      data.push({ type: 'header', title: 'Artists' });
      results.artists.forEach(artist => data.push({ type: 'artist', data: artist }));
    }
    if (results.albums.length > 0) {
      data.push({ type: 'header', title: 'Albums' });
      results.albums.forEach(album => data.push({ type: 'album', data: album }));
    }
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Search for songs, artists, albums..."
        placeholderTextColor={colors.textSecondary}
        value={query}
        onChangeText={debouncedSearch}
      />
      <FlatList
        data={data}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderItem}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: 10,
  },
  input: {
    height: 40,
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 5,
    color: colors.text,
    paddingHorizontal: 10,
    marginBottom: 10,
  },
  header: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.primary,
    marginTop: 15,
    marginBottom: 5,
    paddingHorizontal: 10,
  },
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
