import { describe, expect, it, vi } from 'vitest';

vi.mock('../../src/api/images', () => ({ generateImage: vi.fn() }));
vi.mock('../../src/storage/image-file', () => ({ persistBase64Image: vi.fn() }));

import { inpaintImage } from '../../src/flows/inpaint-image';

describe('inpaint flow', () => {
  it('returns updated image file uri', async () => {
    const result = await inpaintImage({
      key: 'sk-demo',
      prompt: 'replace sky with sunset',
      imageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
      deps: {
        generateImage: vi
          .fn()
          .mockResolvedValue({ data: { data: [{ b64_json: 'ZmFrZQ==' }] } }),
        persistBase64Image: vi.fn().mockResolvedValue('file://updated.png'),
      },
    });

    expect(result.updatedImageUri).toMatch(/^file:\/\//);
  });
});
