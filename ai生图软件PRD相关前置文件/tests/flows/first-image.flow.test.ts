import { describe, expect, it, vi } from 'vitest';

vi.mock('../../src/api/prompt', () => ({ enhancePrompt: vi.fn() }));
vi.mock('../../src/api/images', () => ({ generateImage: vi.fn() }));
vi.mock('../../src/storage/image-file', () => ({ persistBase64Image: vi.fn() }));

import { generateFirstImage } from '../../src/flows/generate-first-image';

describe('first image flow', () => {
  it('returns succeeded status and file uri', async () => {
    const result = await generateFirstImage({
      prompt: 'hello',
      key: 'sk-demo',
      conversationId: 'c1',
      deps: {
        enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [{ message: { content: 'enhanced prompt' } }] } }),
        generateImage: vi.fn().mockResolvedValue({ data: { data: [{ b64_json: 'ZmFrZQ==' }] } }),
        persistBase64Image: vi.fn().mockResolvedValue('file://image.png'),
      },
    });

    expect(result.status).toBe('succeeded');
    expect(result.imageUri.startsWith('file://')).toBe(true);
  });
});
