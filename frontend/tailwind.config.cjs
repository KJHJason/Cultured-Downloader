const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./index.html",
    "./node_modules/flowbite/**/*.js",
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
    "./src/**/*.{vue,js,ts,jsx,tsx,svelte}",
  ],
  theme: {
    extend: {
      colors: {
        // To override the default colours as flowbite uses gray
        gray: colors.zinc,
        gray2: colors.gray,
      },
      fontSize: {
        tiny: "0.5rem",
      },
    },
  },
  plugins: [
    require("flowbite/plugin"),
  ],
}
