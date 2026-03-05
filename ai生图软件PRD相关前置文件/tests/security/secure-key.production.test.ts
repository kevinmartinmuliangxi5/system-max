import { afterEach, describe, expect, it, vi } from 'vitest';

const originalNodeEnv = process.env.NODE_ENV;

afterEach(() => {
  process.env.NODE_ENV = originalNodeEnv;
  vi.resetModules();
  vi.clearAllMocks();
});

describe('secure key in production', () => {
  it('does not allow insecure fallback when secure store is unavailable', async () => {
    process.env.NODE_ENV = 'production';

    vi.doMock('expo-secure-store', () => ({
      setItemAsync: undefined,
      getItemAsync: undefined,
    }));

    const { getApiKey, setApiKey } = await import('../../src/security/secure-key');

    await expect(setApiKey('sk-demo')).rejects.toThrow(
      'Secure storage unavailable in production environment.'
    );
    await expect(getApiKey()).resolves.toBeNull();
  });
});
