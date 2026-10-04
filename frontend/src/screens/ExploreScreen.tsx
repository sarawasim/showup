import React from 'react';
import { PlaceholderScreen, NavButton } from '../components/ui/PlaceholderScreen';
import { TabScreenProps } from '../navigation/types';

export function ExploreScreen({ navigation }: TabScreenProps<'Explore'>) {
  return (
    <PlaceholderScreen title="Explore">
      <NavButton label="Search" onPress={() => navigation.navigate('Search')} />
      <NavButton label="Open a game" onPress={() => navigation.navigate('GameDetails', { gameId: 'demo-2' })} />
    </PlaceholderScreen>
  );
}