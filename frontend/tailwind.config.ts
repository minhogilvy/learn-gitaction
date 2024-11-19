import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        colgate: ["ColgateReady", "sans-serif"],
      },
      colors: {
        bodyText: "#333333",
        default: "#202020",
        red: {
          25: "#F8D9DB",
          50: "#ED999E",
          100: "#D2010D"
        },
        grey: "#757575",
        gray: {
          25: "#F3F3F3",
          50: "#D6D6D6",
          75: "#959392",
          100: "#595655"
        },
        dark: "#282828"
      },
      backgroundImage: {
        dropdown: "url(/images/dropdown.svg)",
      },
      backgroundPosition: {
        dropdown: "right 20px center",
      },
      backgroundSize: {
        dropdown: "24px",
      },
      zIndex: {
        modal: "1000"
      },
      dropShadow: {
        modal: "0 2px 10px rgb(0 0 0 / 0.08)"
      },
      maxWidth: {
        "vw": "768px",
      },
      screens: {
        md: "768px",
      }
    },
  },
  plugins: [],
};
export default config;
