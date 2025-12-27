import React, { useState, useEffect } from 'react';
import { FlatList, Text, StyleSheet, ActivityIndicator } from 'react-native';
import apiClient from '../services/api';
import { colors } from '../theme';
import { useAuth } from '../context/AuthContext';

export default function AlbumList() {
  const { isConnected } = useAuth();
  const [albums, setAlbums] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAlbums = async () => {
      if (isConnected) {
        setLoading(true);
        try {
          const response = await apiClient.get('/library/albums');
          setAlbums(response.data);
        } catch (error) {
          console.error("Failed to fetch albums:", error);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchAlbums();
  }, [isConnected]);

  if (loading) {
    return <ActivityIndicator size="large" color={colors.primary} />;
  }

  return (
    <FlatList
      data={albums}
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
