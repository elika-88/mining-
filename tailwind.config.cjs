module.exports = {
  content: ["./index.html", "./app.js"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["Cascadia Mono", "SFMono-Regular", "Consolas", "monospace"],
      },
      colors: {
        canvas: "#F8F9FA",
        surface: "#FFFFFF",
        subtle: "#F1F3F5",
        line: "#E9ECEF",
        subtext: "#6C757D",
        heavy: "#212529",
      },
    },
  },
};
