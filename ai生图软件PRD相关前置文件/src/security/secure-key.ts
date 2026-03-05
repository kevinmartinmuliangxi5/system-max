import * as SecureStore from 'expo-secure-store';

const KEY = 'siliconflow_api_key';
let memoryKey: string | undefined;

function hasSecureStore() {
  return (
    typeof (SecureStore as { setItemAsync?: unknown }).setItemAsync === 'function' &&
    typeof (SecureStore as { getItemAsync?: unknown }).getItemAsync === 'function'
  );
}

function hasWebStorage() {
  return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
}

function allowInsecureFallback() {
  return process.env.NODE_ENV !== 'production';
}

export async function setApiKey(key: string) {
  if (hasSecureStore()) {
    try {
      await SecureStore.setItemAsync(KEY, key);
      return;
    } catch {
      // Fall through to web/local fallback.
    }
  }

  if (hasWebStorage()) {
    if (allowInsecureFallback()) {
      window.localStorage.setItem(KEY, key);
      return;
    }
    throw new Error('Secure storage unavailable in production environment.');
  }

  if (!allowInsecureFallback()) {
    throw new Error('Secure storage unavailable in production environment.');
  }

  memoryKey = key;
}

export async function getApiKey() {
  if (hasSecureStore()) {
    try {
      return await SecureStore.getItemAsync(KEY);
    } catch {
      // Fall through to web/local fallback.
    }
  }

  if (hasWebStorage()) {
    if (allowInsecureFallback()) {
      return window.localStorage.getItem(KEY);
    }
    return null;
  }

  if (!allowInsecureFallback()) {
    return null;
  }

  return memoryKey ?? null;
}
