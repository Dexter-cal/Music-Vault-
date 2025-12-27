import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/api';

export default function LibraryScreen() {
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

  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Text>Please connect to a PC from the Devices tab.</Text>
      </View>
    );
  }

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Artists</Text>
      <FlatList
        data={artists}
        keyExtractor={(item) => item}
        renderItem={({ item }) => <Text style={styles.item}>{item}</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 50,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  item: {
    padding: 10,
    fontSize: 18,
  },
});
