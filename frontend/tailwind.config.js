module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'navigation': '#5e057e',
        'primary-color': '#5e057e',
        'primary-color-hover': '#5e057ede',
        'secondary-color': '#c299d0',
        'secondary-color-hover': '#c299d0de',
        'positive-button': '#04A118',
        'negative-button': '#DE5147',
        'product-box': '#F8F8F8',
        'other-boxes': '#C9D9C9',
        'text': '#000000',
        'inactive': '#9E9E9E',
        'vipps-main': '#ff5b24',
        'stripe-main': '#6772E5 ',
        'stripe-darker': '#5C65CC',
        'light': '#04A118',
        'transparent-text': '#00000000',
      }
    },
  },
  plugins: [],
}
