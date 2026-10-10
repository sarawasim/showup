import { CustomTheme, useTheme } from "@react-navigation/native";
import { AppScreenProps } from "../navigation/types";
import { StyleSheet, View, Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Button from "../components/ui/Button";
import FormInput from "../components/ui/FormInput";
import TittleAndSubtitle from "../components/ui/TittleAndSubtitle";

const RegisterScreen = ({ navigation }: AppScreenProps<"Register">) => {
	const theme = useTheme();
	const styles = getStyles(theme);

	return (
		<SafeAreaView style={styles.screen}>
			<View style={{ alignSelf: "center" }}>
				<TittleAndSubtitle
					titleText="Register"
					subtitleText="Create an account to start hosting and joining games"
				/>
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
						label="Full Name"
						placeholder="Full Name"
						textContentType="name"
						autoCapitalize="words"
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
					<FormInput
						label="Confirm Password"
						placeholder="Confirm Password"
						secureTextEntry={true}
						textContentType="password"
						autoCorrect={false}
						autoCapitalize="none"
					/>
				</View>
				<Button
					variant="primary"
					onPress={() =>
						navigation.replace("Tabs", { screen: "Home" })
					}
				>
					Register
				</Button>
				<Text style={styles.footerText}>
					Already have an account?{" "}
					<Text
						style={{ color: theme.colors.textSecondary }}
						onPress={() => navigation.navigate("Login")}
					>
						Log In
					</Text>
				</Text>
			</View>
		</SafeAreaView>
	);
};

export default RegisterScreen;

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
		footerText: {
			color: theme.colors.text,
			fontSize: 16,
			textAlign: "center",
			fontWeight: 600,
		},
	});
