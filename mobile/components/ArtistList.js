import React, { useState, useEffect } from 'react';
import { FlatList, Text, StyleSheet, ActivityIndicator } from 'react-native';
import apiClient from '../services/api';
import { colors } from '../theme';
import { useAuth } from '../context/AuthContext';

export default function ArtistList() {
  const { isConnected } = useAuth();
  const [artists, setArtists] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchArtists = async () => {
      if (isConnected) {
        setLoading(true);
        try {
          const response = await apiClient.get('/library/artists');
          setArtists(response.data);
        } catch (error) {
          console.error("Failed to fetch artists:", error);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchArtists();
  }, [isConnected]);

  if (loading) {
    return <ActivityIndicator size="large" color={colors.primary} />;
  }

  return (
    <FlatList
      data={artists}
      keyExtractor={(item) => item}
      renderItem={({ item }) => <Text style={styles.item}>{item}</Text>}
    />
  );
}

const styles = StyleSheet.create({
  item: {
    padding: 15,
    fontSize: 16,
    color: colors.text,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
});
