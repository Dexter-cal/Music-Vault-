import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import LibraryScreen from './screens/LibraryScreen';
import SearchScreen from './screens/SearchScreen';
import NowPlayingScreen from './screens/NowPlayingScreen';
import PlaylistsScreen from './screens/PlaylistsScreen';
import DevicesNavigator from './navigation/DevicesNavigator';
import { AuthProvider, useAuth } from './context/AuthContext';

const Tab = createBottomTabNavigator();

function AppContent() {
  const { loadToken } = useAuth();

  useEffect(() => {
    loadToken();
  }, []);

  return (
    <Tab.Navigator>
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
      <NavigationContainer>
        <AppContent />
      </NavigationContainer>
    </AuthProvider>
  );
}
