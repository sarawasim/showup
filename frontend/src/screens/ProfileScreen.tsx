import React from 'react';
import { PlaceholderScreen, NavButton } from '../components/ui/PlaceholderScreen';
import { TabScreenProps } from '../navigation/types';

export function ProfileScreen({ navigation }: TabScreenProps<'Profile'>) {
  return (
    <PlaceholderScreen title="Profile">
      <NavButton label="Log out" onPress={() => navigation.replace('Login')} />
    </PlaceholderScreen>
  );
}