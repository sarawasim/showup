import React from 'react';
import { PlaceholderScreen, NavButton } from '../components/ui/PlaceholderScreen';
import { AppScreenProps } from '../navigation/types';

export function LoginScreen({ navigation }: AppScreenProps<'Login'>) {
  return (
    <PlaceholderScreen title="Login">
      <NavButton label="Log in" onPress={() => navigation.replace('Tabs', { screen: 'Home' })} />
      <NavButton label="Go to Sign up" onPress={() => navigation.navigate('Signup')} />
    </PlaceholderScreen>
  );
}