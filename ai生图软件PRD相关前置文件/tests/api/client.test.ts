import { describe, expect, it, vi } from 'vitest';

import { api } from '../../src/api/client';

describe('api client', () => {
  it('posts to siliconflow base URL with json payload', async () => {
    const fetchSpy = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({ ok: true }),
      } as Response);

    const result = await api.post('/v1/test', { hello: 'world' }, {
      headers: { Authorization: 'Bearer sk-demo' },
    });

    expect(fetchSpy).toHaveBeenCalledWith(
      'https://api.siliconflow.cn/v1/test',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
          Authorization: 'Bearer sk-demo',
        }),
      })
    );
    expect(result.status).toBe(200);
    expect(result.data).toEqual({ ok: true });
  });

  it('throws api-style error on non-2xx response', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ message: 'Unauthorized' }),
    } as Response);

    await expect(
      api.post('/v1/test', { hello: 'world' }, {
        headers: { Authorization: 'Bearer bad' },
      })
    ).rejects.toMatchObject({
      response: {
        status: 401,
      },
    });
  });

  it('marks timeout aborts with TIMEOUT code', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue({ name: 'AbortError' });

    await expect(api.post('/v1/test', { hello: 'world' })).rejects.toMatchObject({
      code: 'TIMEOUT',
    });
  });
});
