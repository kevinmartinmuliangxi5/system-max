import { describe, expect, it, vi } from 'vitest';

vi.mock('expo-secure-store', () => ({
  setItemAsync: vi.fn().mockResolvedValue(undefined),
  getItemAsync: vi.fn().mockResolvedValue('sk-demo'),
}));

import * as SecureStore from 'expo-secure-store';
import { getApiKey, setApiKey } from '../../src/security/secure-key';

describe('secure key', () => {
  it('stores and retrieves key from secure store', async () => {
    await setApiKey('sk-demo');
    await getApiKey();

    expect(SecureStore.setItemAsync).toHaveBeenCalledWith('siliconflow_api_key', 'sk-demo');
    expect(SecureStore.getItemAsync).toHaveBeenCalledWith('siliconflow_api_key');
  });
});
