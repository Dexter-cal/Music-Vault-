import axios from 'axios';
import * as FileSystem from 'expo-file-system';
import { Asset } from 'expo-asset';

let httpsAgent;

export const initializeApiClient = async () => {
  try {
    const certAsset = Asset.fromModule(require('../assets/server.crt'));
    await certAsset.downloadAsync();
    const certUri = certAsset.uri;

    const certContent = await FileSystem.readAsStringAsync(certUri);

    console.log("Certificate loaded. In a real app, we would use this for pinning.");

  } catch (error) {
    console.error("Failed to initialize API client:", error);
  }
};

const apiClient = axios.create({
  // The baseURL will be set dynamically.
  // For development with self-signed certificates, we might need to disable SSL verification.
  // This is not recommended for production.
  httpsAgent: __DEV__ ? { rejectUnauthorized: false } : undefined,
});

export const setApiBaseUrl = (url) => {
  apiClient.defaults.baseURL = url;
};

export const checkConnection = async (token) => {
  try {
    const response = await apiClient.post('/check_connection', { token });
    return response.data;
  } catch (error) {
    console.error("Connection check failed:", error);
    return { status: 'error', message: 'Failed to connect to the server.' };
  }
};

export default apiClient;
