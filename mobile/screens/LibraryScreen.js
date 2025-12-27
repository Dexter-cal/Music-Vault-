import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { useAuth } from '../context/AuthContext';
import { colors } from '../theme';
import TrackList from '../components/TrackList';
import ArtistList from '../components/ArtistList';
import AlbumList from '../components/AlbumList';

const Tab = createMaterialTopTabNavigator();

export default function LibraryScreen() {
  const { isConnected } = useAuth();

  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Please connect to a PC from the Devices tab.</Text>
      </View>
    );
  }

  return (
    <Tab.Navigator
      screenOptions={{
        tabBarStyle: { backgroundColor: colors.surface },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarIndicatorStyle: { backgroundColor: colors.primary },
      }}
    >
      <Tab.Screen name="All Music" component={TrackList} />
      <Tab.Screen name="Artists" component={ArtistList} />
      <Tab.Screen name="Albums" component={AlbumList} />
    </Tab.Navigator>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: colors.textSecondary,
  },
});
