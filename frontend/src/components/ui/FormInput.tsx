import { CustomTheme, useTheme } from "@react-navigation/native";
import {
	StyleProp,
	StyleSheet,
	Text,
	TextInput,
	TextStyle,
	TextInputProps,
	View,
} from "react-native";

interface FormInputProps extends TextInputProps {
	label: string;
	inputStyle?: StyleProp<TextStyle>;
	labelStyle?: StyleProp<TextStyle>;
}

const FormInput: React.FC<FormInputProps> = ({
	label,
	inputStyle,
	labelStyle,
	...inputProps
}) => {
	const theme = useTheme();
	const styles = getStyles(theme);

	return (
		<View style={styles.container}>
			<Text style={[styles.label, labelStyle]}>{label}</Text>
			<TextInput
				style={[styles.input, inputStyle]}
				placeholderTextColor={theme.colors.textMuted}
				{...inputProps}
			></TextInput>
		</View>
	);
};

export default FormInput;

const getStyles = (theme: CustomTheme) =>
	StyleSheet.create({
		container: {
			display: "flex",
			gap: 3,
		},
		label: {
			color: theme.colors.textMuted,
			fontSize: 12,
		},
		input: {
			borderWidth: 1,
			borderColor: "#3C3C3C",
			backgroundColor: "#2B2B2B",
			color: theme.colors.text,
			fontSize: 14,
			padding: 10,
		},
	});
