import React, { createContext, useState, useContext } from 'react';
import * as SecureStore from 'expo-secure-store';
import apiClient, { checkConnection, initializeApiClient, setApiBaseUrl } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [apiUrl, setApiUrlState] = useState('');

  const setApiUrl = (url) => {
    setApiUrlState(url);
    setApiBaseUrl(url);
  };

  const connectToServer = async (scannedToken) => {
    const result = await checkConnection(scannedToken);
    if (result.status === 'ok') {
      await SecureStore.setItemAsync('authToken', scannedToken);
      setToken(scannedToken);
      setIsConnected(true);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${scannedToken}`;
      return true;
    }
    return false;
  };

  const loadToken = async () => {
    const storedToken = await SecureStore.getItemAsync('authToken');
    if (storedToken) {
      setToken(storedToken);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
      // We can't check the connection here without the API URL.
      // The user will need to re-enter the IP on app start.
      // A more advanced implementation could store the last used IP.
    }
    initializeApiClient();
  };

  return (
    <AuthContext.Provider value={{ token, isConnected, apiUrl, setApiUrl, connectToServer, loadToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
