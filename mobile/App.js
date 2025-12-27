import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'react-native';
import LibraryScreen from './screens/LibraryScreen';
import SearchScreen from './screens/SearchScreen';
import NowPlayingScreen from './screens/NowPlayingScreen';
import PlaylistsScreen from './screens/PlaylistsScreen';
import DevicesNavigator from './navigation/DevicesNavigator';
import { AuthProvider, useAuth } from './context/AuthContext';
import { PlayerProvider } from './context/PlayerContext';
import { theme, colors } from './theme';

const Tab = createBottomTabNavigator();

function AppContent() {
  const { loadToken } = useAuth();

  useEffect(() => {
    loadToken();
  }, []);

  return (
    <Tab.Navigator
      screenOptions={{
        tabBarStyle: { backgroundColor: colors.surface },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        headerStyle: { backgroundColor: colors.surface },
        headerTintColor: colors.text,
      }}
    >
      <Tab.Screen name="Library" component={LibraryScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Now Playing" component={NowPlayingScreen} />
      <Tab.Screen name="Playlists" component={PlaylistsScreen} />
      <Tab.Screen name="Devices" component={DevicesNavigator} options={{ headerShown: false }} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <PlayerProvider>
        <NavigationContainer theme={theme}>
          <StatusBar barStyle="light-content" />
          <AppContent />
        </NavigationContainer>
      </PlayerProvider>
    </AuthProvider>
  );
}
