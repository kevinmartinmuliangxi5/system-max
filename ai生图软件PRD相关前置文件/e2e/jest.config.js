module.exports = {
  rootDir: '..',
  testMatch: ['<rootDir>/e2e/**/*.e2e.ts'],
  testTimeout: 120000,
  preset: 'ts-jest',
  transform: {
    '^.+\\.ts$': ['ts-jest', { isolatedModules: true }],
  },
  reporters: ['detox/runners/jest/reporter'],
  testEnvironment: 'detox/runners/jest/testEnvironment',
  setupFilesAfterEnv: ['<rootDir>/e2e/test-setup.ts'],
};

