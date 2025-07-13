module.exports = {
  transform: {
    "^.+\\.jsx?$": "babel-jest",
  },
  moduleNameMapper: {
    "^axios$": require.resolve("axios"),
  },
  testEnvironment: "jsdom",
};
