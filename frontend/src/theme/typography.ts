import { DefaultTheme } from "@react-navigation/native";

export const typography = {
	...DefaultTheme.fonts,
	title: { fontSize: 24, fontWeight: "700" as const },
	body: { fontSize: 16, fontWeight: "400" as const },
	caption: { fontSize: 13, fontWeight: "400" as const },
};
