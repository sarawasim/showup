# ShowUp — Frontend

Expo (React Native) + TypeScript + React Navigation.

## Run it

```bash
cd frontend
npm install
npx expo start
```

Press `i` for the iOS Simulator, `a` for Android, `w` for the browser, or scan the QR code with Expo Go.

- Browser needs this once: `npx expo install react-dom react-native-web`
- Weird behaviour after pulling? `npx expo start -c` clears the cache.
- Type-check before committing: `npx tsc --noEmit`
- Add packages with `npx expo install <package>` (not `npm install`) so versions match Expo.

## Environment variables

Copy `.env.example` to `.env`. Only `EXPO_PUBLIC_` variables reach the app, and they're bundled in where anyone can read them, so never put secrets here.

## Structure

```
App.tsx               # root component
src/
  theme/              # colors, spacing, typography (change the look here)
  navigation/
    types.ts          # every route and its params
    AppNavigator.tsx  # main stack
    MainTabs.tsx      # bottom tabs: Home, Explore, Profile
  screens/            # one file per screen
  components/ui/      # shared building blocks
```

## Adding a screen

1. Create it in `src/screens/`.
2. Add the route to `src/navigation/types.ts` (`MainTabParamList` for a tab, `AppStackParamList` otherwise).
3. Register it in `MainTabs.tsx` or `AppNavigator.tsx`.
4. Use `theme` for colors and spacing instead of hardcoding them.

## Commits

Branch off `main`, prefix commits with `frontend:`, and open a PR for review.
