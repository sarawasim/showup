import { SafeAreaView } from "react-native-safe-area-context";
import { StyleSheet, Text, View } from "react-native";
import { AppScreenProps } from "../navigation/types";
import FormInput from "../components/ui/FormInput";
import { CustomTheme, useTheme } from "@react-navigation/native";
import Button from "../components/ui/Button";

const SigninScreen = ({ navigation }: AppScreenProps<"Login">) => {
	const theme = useTheme();
	const styles = getStyles(theme);

	return (
		<SafeAreaView style={styles.screen}>
			<View style={{ alignSelf: "center" }}>
				<Text style={styles.titleText}>Login</Text>
				<Text style={styles.subtitleText}>
					Enter your email and password to log in
				</Text>
			</View>
			<View style={{ display: "flex", gap: 25 }}>
				<View style={{ display: "flex", gap: 10 }}>
					<FormInput
						label="Email"
						placeholder="Email"
						autoCapitalize="none"
						keyboardType="email-address"
						autoCorrect={false}
					/>
					<FormInput
						label="Password"
						placeholder="Password"
						secureTextEntry={true}
						textContentType="password"
						autoCorrect={false}
						autoCapitalize="none"
					/>
				</View>
				<Button
					variant="primary"
					onPress={() => navigation.navigate("Register")}
				>
					Login
				</Button>
			</View>
		</SafeAreaView>
	);
};

export default SigninScreen;

const getStyles = (theme: CustomTheme) =>
	StyleSheet.create({
		screen: {
			display: "flex",
			flex: 1,
			justifyContent: "flex-start",
			marginTop: 50,
			marginBottom: 50,
			gap: 30,
			width: "90%",
			alignSelf: "center",
		},
		titleText: {
			fontWeight: 600,
			color: theme.colors.text,
			fontSize: 32,
			textAlign: "center",
		},
		subtitleText: {
			fontWeight: 400,
			color: theme.colors.textMuted,
			fontSize: 16,
			textAlign: "center",
		},
	});
