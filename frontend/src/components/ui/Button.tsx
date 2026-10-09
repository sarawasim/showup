import {
	Pressable,
	PressableProps,
	StyleProp,
	Text,
	TextStyle,
} from "react-native";

interface ButtonProps extends PressableProps {
	buttonStyle: StyleProp<TextStyle>;
	textStyle: StyleProp<TextStyle>;
	children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
	buttonStyle,
	textStyle,
	children,
	...buttonProps
}) => {
	return (
		<Pressable style={buttonStyle} {...buttonProps}>
			<Text style={textStyle}>{children}</Text>
		</Pressable>
	);
};

export default Button;
