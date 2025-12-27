import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import DevicesScreen from '../screens/DevicesScreen';
import ScannerScreen from '../screens/ScannerScreen';

const Stack = createStackNavigator();

export default function DevicesNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Devices" component={DevicesScreen} />
      <Stack.Screen name="Scanner" component={ScannerScreen} />
    </Stack.Navigator>
  );
}
