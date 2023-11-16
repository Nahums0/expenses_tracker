module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false,
  theme: {
    extend: {
      width: {
        "2/9": "22.2222%",
      },
      height: {
        "0.5/10": "5%",
        "1/10": "10%",
        "7/10": "70%",
        "9/10": "90%",
        "9.5/10": "95%",
      },
      spacing: {
        "1/24": "4.1667%",
      },
      borderWidth: {
        1: "1px",
      },
      colors: {
        main: "#0D4249",
        bgColor: "#F3F1EC",
        navBg: "#2b8c90d4",
      },
      fontFamily: {
        julius: ['"Julius Sans One"', "sans-serif"],
      },
    },
  },
  variants: {},
  plugins: [],
};
