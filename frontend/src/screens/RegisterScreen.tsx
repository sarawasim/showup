import {
	PlaceholderScreen,
	NavButton,
} from "../components/ui/PlaceholderScreen";
import { AppScreenProps } from "../navigation/types";

export default function RegisterScreen({ navigation }: AppScreenProps<"Register">) {
	return (
		<PlaceholderScreen title="Sign up">
			<NavButton
				label="Create account"
				onPress={() => navigation.replace("Tabs", { screen: "Home" })}
			/>
			<NavButton
				label="Back to Login"
				onPress={() => navigation.goBack()}
			/>
		</PlaceholderScreen>
	);
}
