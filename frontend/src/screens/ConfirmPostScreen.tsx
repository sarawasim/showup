import React from 'react';
import { PlaceholderScreen, NavButton } from '../components/ui/PlaceholderScreen';
import { AppScreenProps } from '../navigation/types';

export function ConfirmPostScreen({ navigation, route }: AppScreenProps<'ConfirmPost'>) {
  return (
    <PlaceholderScreen title={`Confirm post (${route.params.draftId})`}>
      <NavButton label="Post game" onPress={() => navigation.popTo('Tabs', { screen: 'Home' })} />
    </PlaceholderScreen>
  );
}