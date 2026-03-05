import { api } from './client';

type ImagePayload = {
  model: string;
  prompt: string;
  image?: string;
  mask?: string;
  size?: string;
  response_format?: string;
};

type ImageResponse = {
  data?: Array<{ b64_json?: string }>;
};

export function generateImage(key: string, payload: ImagePayload) {
  return api.post<ImageResponse>('/v1/images/generations', payload, {
    headers: { Authorization: `Bearer ${key}` },
  });
}
