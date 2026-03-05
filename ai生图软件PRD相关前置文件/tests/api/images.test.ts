import { describe, expect, it, vi } from 'vitest';
import { api } from '../../src/api/client';
import { generateImage } from '../../src/api/images';

describe('images api', () => {
  it('posts to /v1/images/generations with bearer token', async () => {
    const post = vi.spyOn(api, 'post').mockResolvedValue({ data: { ok: true } } as never);

    await generateImage('sk-test', { model: 'black-forest-labs/FLUX.1-Kontext-pro', prompt: 'hello' });

    expect(post).toHaveBeenCalledWith(
      '/v1/images/generations',
      { model: 'black-forest-labs/FLUX.1-Kontext-pro', prompt: 'hello' },
      { headers: { Authorization: 'Bearer sk-test' } }
    );
  });
});
