import React from 'react';
import { PlaceholderScreen, NavButton } from '../components/ui/PlaceholderScreen';
import { AppScreenProps } from '../navigation/types';

export function CreatePostScreen({ navigation }: AppScreenProps<'CreatePost'>) {
  return (
    <PlaceholderScreen title="Create a post">
      <NavButton label="Continue" onPress={() => navigation.navigate('ConfirmPost', { draftId: 'draft-1' })} />
    </PlaceholderScreen>
  );
}