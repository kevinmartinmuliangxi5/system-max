import { useCallback, useEffect, useMemo, useState } from 'react';

import { mapErrorMessage } from '../errors/map-error';
import { generateFirstImage } from '../flows/generate-first-image';
import { getApiKey, setApiKey } from '../security/secure-key';
import { setLatestResult } from './latest-result.store';

const ENV_API_KEY =
  process.env.NODE_ENV === 'production'
    ? ''
    : (process.env.EXPO_PUBLIC_SILICONFLOW_API_KEY?.trim() ?? '');
const DEFAULT_CONVERSATION_ID = 'conv_primary';

type ChatGenerateState = {
  status: 'idle' | 'submitting' | 'succeeded' | 'failed';
  prompt: string;
  apiKeyInput: string;
  hasApiKey: boolean;
  imageUri?: string;
  enhancedPrompt?: string;
  errorMessage?: string;
};

function readStatusCode(error: unknown): number | undefined {
  const status = (error as { response?: { status?: number } })?.response?.status;
  return typeof status === 'number' ? status : undefined;
}

function readErrorCode(error: unknown): string | undefined {
  const code = (error as { code?: string })?.code;
  return typeof code === 'string' ? code : undefined;
}

export function useChatStore() {
  const [state, setState] = useState<ChatGenerateState>({
    status: 'idle',
    prompt: '',
    apiKeyInput: ENV_API_KEY,
    hasApiKey: ENV_API_KEY.length > 0,
  });

  useEffect(() => {
    let mounted = true;
    getApiKey()
      .then((key) => {
        const resolved = key?.trim() || ENV_API_KEY;
        if (!mounted) {
          return;
        }
        setState((prev) => ({
          ...prev,
          hasApiKey: Boolean(resolved),
          apiKeyInput: resolved || prev.apiKeyInput,
        }));
      })
      .catch(() => {
        // Keep default state when secure store is unavailable.
      });
    return () => {
      mounted = false;
    };
  }, []);

  const canSubmit = useMemo(
    () =>
      state.status !== 'submitting' &&
      state.prompt.trim().length > 0 &&
      state.hasApiKey,
    [state.status, state.prompt, state.hasApiKey]
  );

  const setPrompt = useCallback((prompt: string) => {
    setState((prev) => ({ ...prev, prompt, errorMessage: undefined }));
  }, []);

  const setApiKeyInput = useCallback((apiKeyInput: string) => {
    setState((prev) => ({ ...prev, apiKeyInput, errorMessage: undefined }));
  }, []);

  const persistApiKey = useCallback(async () => {
    const key = state.apiKeyInput.trim();
    if (!key) {
      setState((prev) => ({
        ...prev,
        hasApiKey: false,
        errorMessage: 'Please enter an API key before saving.',
      }));
      return;
    }
    try {
      await setApiKey(key);
      setState((prev) => ({
        ...prev,
        hasApiKey: true,
        errorMessage: undefined,
      }));
    } catch {
      setState((prev) => ({
        ...prev,
        hasApiKey: false,
        errorMessage: 'Failed to save API key in this environment.',
      }));
    }
  }, [state.apiKeyInput]);

  const submitPrompt = useCallback(async () => {
    const prompt = state.prompt.trim();
    if (!prompt || state.status === 'submitting') {
      return;
    }

    const key = (await getApiKey())?.trim() || ENV_API_KEY;
    if (!key) {
      setState((prev) => ({
        ...prev,
        status: 'failed',
        hasApiKey: false,
        errorMessage: 'Missing API key. Save your key first.',
      }));
      return;
    }

    setState((prev) => ({
      ...prev,
      status: 'submitting',
      hasApiKey: true,
      errorMessage: undefined,
    }));

    try {
      const result = await generateFirstImage({
        prompt,
        key,
        conversationId: DEFAULT_CONVERSATION_ID,
      });
      setLatestResult({
        imageUri: result.imageUri,
        prompt: result.prompt,
      });

      setState((prev) => ({
        ...prev,
        status: 'succeeded',
        imageUri: result.imageUri,
        enhancedPrompt: result.prompt,
        errorMessage: undefined,
      }));
    } catch (error) {
      setState((prev) => ({
        ...prev,
        status: 'failed',
        errorMessage: mapErrorMessage({
          status: readStatusCode(error),
          code: readErrorCode(error),
        }),
      }));
    }
  }, [state.prompt, state.status]);

  return {
    state,
    canSubmit,
    setPrompt,
    setApiKeyInput,
    persistApiKey,
    submitPrompt,
  };
}
