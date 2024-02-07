/** @type {import('tailwindcss').Config} */
export default {
  content: ["../dream_blog/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography")],
};
