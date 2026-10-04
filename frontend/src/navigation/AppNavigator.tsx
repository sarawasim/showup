import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AppStackParamList } from './types';
import { stackScreenOptions } from './options';
import { MainTabs } from './MainTabs';
import { LoginScreen } from '../screens/LoginScreen';
import { SignupScreen } from '../screens/SignupScreen';
import { SearchScreen } from '../screens/SearchScreen';
import { CreatePostScreen } from '../screens/CreatePostScreen';
import { ConfirmPostScreen } from '../screens/ConfirmPostScreen';
import { GameDetailsScreen } from '../screens/GameDetailsScreen';


const Stack = createNativeStackNavigator<AppStackParamList>();

export function AppNavigator() {
  return (
      <Stack.Navigator initialRouteName="Login" screenOptions={stackScreenOptions}>
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Signup" component={SignupScreen} options={{ title: 'Sign up' }} />
        <Stack.Screen name="Tabs" component={MainTabs} options={{ headerShown: false }} />
        <Stack.Screen name="Search" component={SearchScreen} />
        <Stack.Screen name="CreatePost" component={CreatePostScreen} options={{ title: 'Create a post' }} />
        <Stack.Screen name="ConfirmPost" component={ConfirmPostScreen} options={{ title: 'Confirm post' }} />
        <Stack.Screen name="GameDetails" component={GameDetailsScreen} options={{ title: 'Game details' }} />
    </Stack.Navigator>
  );
}