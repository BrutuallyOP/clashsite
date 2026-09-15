/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        // Ink + linen, with a muted moss accent — deliberately not the
        // cream/terracotta or near-black/acid-green combos that show up
        // by default in generated UI.
        ink: {
          900: "#1C1E1B",
          700: "#3A3D38",
          500: "#6B6E67",
        },
        linen: {
          50: "#FBFAF6",
          100: "#F3F1EA",
        },
        moss: {
          600: "#4C6B4F",
          500: "#5D7F60",
          100: "#E4EBE1",
        },
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        body: ["Source Sans 3", "system-ui", "sans-serif"],
      },
      borderRadius: {
        sm: "4px",
        md: "6px",
      },
    },
  },
  plugins: [],
};
