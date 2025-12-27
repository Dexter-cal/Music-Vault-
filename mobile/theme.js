export const colors = {
  background: '#121212', // A dark, near-black for backgrounds
  surface: '#1E1E1E',   // A slightly lighter dark for cards, tabs, etc.
  primary: '#BB86FC',   // A vibrant purple for primary actions and highlights
  secondary: '#03DAC6', // A teal for secondary accents
  text: '#FFFFFF',       // White for primary text
  textSecondary: '#B3B3B3', // A light grey for secondary or muted text
  error: '#CF6679',      // A reddish pink for error messages
  border: '#2A2A2A',     // A dark grey for borders
};

export const theme = {
  dark: true,
  colors: {
    primary: colors.primary,
    background: colors.background,
    card: colors.surface,
    text: colors.text,
    border: colors.border,
    notification: colors.primary,
  },
};
