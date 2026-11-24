import { ButtonProps } from ".";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    // @default primary
    variant?: 'primary' | 'secondary' | 'idle' | 'positive' | 'negative';
    // @default medium
    size? : 'default' | 'small';
    // @default: default
    state?: 'default' | 'disabled' | 'loading';
    children: React.ReactNode;
}

export type { ButtonProps };