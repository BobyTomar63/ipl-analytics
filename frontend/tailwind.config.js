/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ipl-blue': '#003366',
        'ipl-gold': '#FFD700',
        'ipl-orange': '#FF6B00',
      }
    },
  },
  plugins: [],
}
