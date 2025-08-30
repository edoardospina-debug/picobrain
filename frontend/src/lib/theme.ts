// PicoBrain Theme Configuration
// Based on Dashboard's modern v0 styling & PicoClinics color palette

export const theme = {
  // Color palette
  colors: {
    primary: {
      50: '#ecfeff',
      100: '#cffafe',
      200: '#a5f3fc',
      300: '#67e8f9',
      400: '#22d3ee',
      500: '#06b6d4', // cyan-500
      600: '#0891b2',
      700: '#0e7490',
      800: '#155e75',
      900: '#164e63',
    },
    secondary: {
      400: '#60a5fa',
      500: '#3b82f6', // blue-500
      600: '#2563eb',
    },
    gradient: {
      primary: 'from-cyan-500 to-blue-500',
      primaryHover: 'from-cyan-600 to-blue-600',
      background: 'from-gray-50 via-white to-cyan-50/20',
    },
  },

  // Glass effect styles
  glass: {
    card: 'bg-white/80 backdrop-blur-md border-white/50',
    cardHover: 'hover:shadow-lg transition-all duration-300',
    modal: 'bg-white/95 backdrop-blur-md',
    header: 'bg-white/80 backdrop-blur-md border-b border-gray-200',
    sidebar: 'bg-white/95 backdrop-blur-md border-r border-gray-200',
  },

  // Animation configurations
  animations: {
    fadeIn: {
      initial: { opacity: 0, y: 20 },
      animate: { opacity: 1, y: 0 },
      transition: { duration: 0.5 },
    },
    slideIn: {
      initial: { opacity: 0, x: -20 },
      animate: { opacity: 1, x: 0 },
      exit: { opacity: 0, x: -20 },
    },
    hover: {
      whileHover: { y: -4 },
      transition: { duration: 0.2 },
    },
    pulse: 'animate-pulse',
    spin: 'animate-spin',
  },

  // Common styles
  styles: {
    pageBackground: 'min-h-screen bg-gradient-to-br from-gray-50 via-white to-cyan-50/20',
    button: {
      primary: 'bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-medium px-4 py-2 rounded-lg transition-all duration-300',
      secondary: 'bg-white/80 backdrop-blur-sm border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium px-4 py-2 rounded-lg transition-all duration-300',
      ghost: 'hover:bg-gray-100/50 text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg transition-all duration-300',
    },
    input: 'w-full px-4 py-2 bg-white/50 backdrop-blur-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-300',
    table: {
      wrapper: 'bg-white/80 backdrop-blur-md border-white/50 rounded-lg shadow-sm overflow-hidden',
      header: 'bg-gray-50/50 backdrop-blur-sm border-b border-gray-200',
      row: 'hover:bg-gray-50/50 transition-colors duration-200',
    },
  },
};

export default theme;