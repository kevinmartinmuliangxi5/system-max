import { api } from './client';

type PromptPayload = {
  model: string;
  messages: Array<{ role: string; content: string }>;
  temperature?: number;
};

type PromptResponse = {
  choices?: Array<{ message?: { content?: string } }>;
};

export function enhancePrompt(key: string, payload: PromptPayload) {
  return api.post<PromptResponse>('/v1/chat/completions', payload, {
    headers: { Authorization: `Bearer ${key}` },
  });
}
