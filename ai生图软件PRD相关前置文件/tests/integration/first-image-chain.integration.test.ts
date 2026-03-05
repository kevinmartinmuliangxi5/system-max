import { describe, expect, it, vi } from 'vitest';

vi.mock('expo-file-system', () => ({
  cacheDirectory: 'file://cache/',
  EncodingType: { Base64: 'base64' },
  writeAsStringAsync: vi.fn().mockResolvedValue(undefined),
}));

import * as FileSystem from 'expo-file-system';
import { api } from '../../src/api/client';
import { generateFirstImage } from '../../src/flows/generate-first-image';

describe('first-image integration chain', () => {
  it('runs prompt enhance -> image generate -> base64 persist', async () => {
    const postSpy = vi
      .spyOn(api, 'post')
      .mockResolvedValueOnce({
        data: {
          id: 'prompt-1',
          choices: [{ message: { content: 'enhanced prompt' } }],
        },
      } as never)
      .mockResolvedValueOnce({
        data: { data: [{ b64_json: 'ZmFrZQ==' }] },
      } as never);

    const result = await generateFirstImage({
      prompt: 'raw prompt',
      key: 'sk-key',
      conversationId: 'conv-1',
    });

    expect(postSpy).toHaveBeenNthCalledWith(
      1,
      '/v1/chat/completions',
      {
        model: 'deepseek-ai/DeepSeek-V3',
        messages: [{ role: 'user', content: 'raw prompt' }],
      },
      { headers: { Authorization: 'Bearer sk-key' } }
    );
    expect(postSpy).toHaveBeenNthCalledWith(
      2,
      '/v1/images/generations',
      {
        model: 'black-forest-labs/FLUX.1-schnell',
        prompt: 'enhanced prompt',
        response_format: 'b64_json',
      },
      { headers: { Authorization: 'Bearer sk-key' } }
    );
    expect(FileSystem.writeAsStringAsync).toHaveBeenCalledWith(
      expect.stringMatching(/^file:\/\/cache\/gen_\d+\.png$/),
      'ZmFrZQ==',
      { encoding: 'base64' }
    );
    expect(result.status).toBe('succeeded');
    expect(result.prompt).toBe('enhanced prompt');
    expect(result.imageUri).toMatch(/^file:\/\/cache\/gen_\d+\.png$/);
  });
});
