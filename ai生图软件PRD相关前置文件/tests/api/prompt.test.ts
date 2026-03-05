import { describe, expect, it, vi } from 'vitest';
import { api } from '../../src/api/client';
import { enhancePrompt } from '../../src/api/prompt';

describe('prompt api', () => {
  it('posts to /v1/chat/completions with bearer token', async () => {
    const post = vi.spyOn(api, 'post').mockResolvedValue({ data: { ok: true } } as never);

    await enhancePrompt('sk-test', { model: 'deepseek-ai/DeepSeek-V3', messages: [] });

    expect(post).toHaveBeenCalledWith(
      '/v1/chat/completions',
      { model: 'deepseek-ai/DeepSeek-V3', messages: [] },
      { headers: { Authorization: 'Bearer sk-test' } }
    );
  });
});
