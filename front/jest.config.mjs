export default {
  transform: {
    "^.+\\.(js|jsx|ts|tsx)$": "babel-jest",
  },
  moduleNameMapper: {
    "\\.module\\.css$": "identity-obj-proxy",
  },
  testEnvironment: "jest-environment-jsdom",
};
