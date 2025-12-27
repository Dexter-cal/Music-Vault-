import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet, Alert, TextInput } from 'react-native';
import { useAuth } from '../context/AuthContext';
import { colors } from '../theme';

export default function DevicesScreen({ navigation, route }) {
  const { isConnected, connectToServer, setApiUrl } = useAuth();
  const [ipAddress, setIpAddress] = useState('');

  useEffect(() => {
    if (route.params?.qrCodeData) {
      const { qrCodeData } = route.params;
      if (!ipAddress) {
        Alert.alert("IP Address Required", "Please enter the PC's IP address before scanning.");
        return;
      }
      setApiUrl(`https://${ipAddress}:5000`);
      const handleConnection = async () => {
        const success = await connectToServer(qrCodeData);
        if (!success) {
          Alert.alert("Connection Failed", "Could not connect to the PC. Please check the server and try again.");
        }
      };
      handleConnection();
    }
  }, [route.params?.qrCodeData]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Devices</Text>
      <Text style={styles.status}>Status: {isConnected ? 'Connected' : 'Disconnected'}</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter PC's IP Address"
        placeholderTextColor={colors.textSecondary}
        value={ipAddress}
        onChangeText={setIpAddress}
        autoCapitalize="none"
        keyboardType="numeric"
      />
      <Button
        title="Connect to PC"
        color={colors.primary}
        onPress={() => {
          if (!ipAddress) {
            Alert.alert("IP Address Required", "Please enter the PC's IP address.");
            return;
          }
          setApiUrl(`https://${ipAddress}:5000`);
          navigation.navigate('Scanner');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 20,
  },
  status: {
    fontSize: 18,
    color: colors.text,
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 40,
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 5,
    color: colors.text,
    marginBottom: 20,
    paddingHorizontal: 10,
  },
});
