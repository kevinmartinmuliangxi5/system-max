import { describe, expect, it, vi } from 'vitest';

vi.mock('../../src/api/prompt', () => ({ enhancePrompt: vi.fn() }));
vi.mock('../../src/api/images', () => ({ generateImage: vi.fn() }));
vi.mock('../../src/storage/image-file', () => ({ persistBase64Image: vi.fn() }));

import { generateFirstImage } from '../../src/flows/generate-first-image';

type FirstImageDeps = NonNullable<Parameters<typeof generateFirstImage>[0]['deps']>;

describe('generateFirstImage unit', () => {
  it('falls back to original prompt when enhancement content is empty', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [] } }),
      generateImage: vi.fn().mockResolvedValue({ data: { data: [{ b64_json: 'ZmFrZQ==' }] } }),
      persistBase64Image: vi.fn().mockResolvedValue('file://img.png'),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveConversationHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-assistant-1' }),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await generateFirstImage({
      prompt: 'raw prompt',
      key: 'sk-demo',
      conversationId: 'c1',
      deps,
    });

    expect(deps.generateImage).toHaveBeenCalledWith('sk-demo', {
      model: 'black-forest-labs/FLUX.1-schnell',
      prompt: 'raw prompt',
      response_format: 'b64_json',
    });
    expect(deps.saveConversationHistory).toHaveBeenCalledWith(
      expect.objectContaining({
        conversationId: 'c1',
        userPrompt: 'raw prompt',
        assistantPrompt: 'raw prompt',
        imageUri: 'file://img.png',
      })
    );
    expect(deps.logRequest).toHaveBeenCalledWith(
      expect.objectContaining({
        requestType: 'image_generation',
        success: 1,
        conversationId: 'c1',
        messageId: 'm-assistant-1',
      })
    );
    expect(result.prompt).toBe('raw prompt');
    expect(result.imageUri).toBe('file://img.png');
  });

  it('retries retriable status codes and records retry count', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [{ message: { content: 'enhanced' } }] } }),
      generateImage: vi
        .fn()
        .mockRejectedValueOnce({ response: { status: 503 } })
        .mockResolvedValueOnce({ data: { data: [{ b64_json: 'ZmFrZQ==' }] } }),
      persistBase64Image: vi.fn().mockResolvedValue('file://img.png'),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveConversationHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-assistant-2' }),
      sleep: vi.fn().mockResolvedValue(undefined),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await generateFirstImage({
      prompt: 'raw prompt',
      key: 'sk-demo',
      conversationId: 'c1',
      deps,
    });

    expect(result.status).toBe('succeeded');
    expect(deps.generateImage).toHaveBeenCalledTimes(2);
    expect(deps.logRequest).toHaveBeenCalledWith(
      expect.objectContaining({
        requestType: 'image_generation',
        success: 1,
        retryCount: 1,
      })
    );
  });

  it('does not retry non-retriable 4xx errors', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [{ message: { content: 'enhanced' } }] } }),
      generateImage: vi.fn().mockRejectedValue({ response: { status: 400 } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveConversationHistory: vi.fn(),
      sleep: vi.fn().mockResolvedValue(undefined),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    await expect(
      generateFirstImage({
        prompt: 'raw prompt',
        key: 'sk-demo',
        conversationId: 'c1',
        deps,
      })
    ).rejects.toMatchObject({ response: { status: 400 } });

    expect(deps.generateImage).toHaveBeenCalledTimes(1);
    expect(deps.sleep).not.toHaveBeenCalled();
  });

  it('rejects when image response fails schema validation', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [{ message: { content: 'enhanced' } }] } }),
      generateImage: vi
        .fn()
        .mockResolvedValue({ data: { data: [{ url: 'https://example.com/image.png' }] } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn(() => {
        throw new Error('Invalid image response schema');
      }),
      saveConversationHistory: vi.fn(),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    await expect(
      generateFirstImage({
        prompt: 'raw prompt',
        key: 'sk-demo',
        conversationId: 'c1',
        deps,
      })
    ).rejects.toThrow('Invalid image response schema');

    expect(deps.validateImageResponse).toHaveBeenCalledTimes(1);
    expect(deps.persistBase64Image).not.toHaveBeenCalled();
  });

  it('uses direct image URL when provider returns url', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({
        data: { id: 'prompt-1', choices: [{ message: { content: 'enhanced' } }] },
      }),
      generateImage: vi
        .fn()
        .mockResolvedValue({ data: { data: [{ url: 'https://example.com/image.png' }] } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ url: string }> }),
      saveConversationHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-assistant-4' }),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await generateFirstImage({
      prompt: 'raw prompt',
      key: 'sk-demo',
      conversationId: 'c1',
      deps,
    });

    expect(result.imageUri).toBe('https://example.com/image.png');
    expect(deps.persistBase64Image).not.toHaveBeenCalled();
  });

  it('does not block failure path on slow log writes', async () => {
    const deps: FirstImageDeps = {
      enhancePrompt: vi.fn().mockResolvedValue({ data: { choices: [] } }),
      generateImage: vi.fn().mockRejectedValue({ response: { status: 503 } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveConversationHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-assistant-3' }),
      sleep: vi.fn().mockResolvedValue(undefined),
      logRequest: vi.fn().mockImplementation(() => new Promise(() => {})),
      logReplay: vi.fn().mockImplementation(() => new Promise(() => {})),
    };

    const startedAt = Date.now();
    await expect(
      generateFirstImage({
        prompt: 'raw prompt',
        key: 'sk-demo',
        conversationId: 'c1',
        deps,
      })
    ).rejects.toBeTruthy();
    const elapsed = Date.now() - startedAt;

    expect(elapsed).toBeLessThan(2500);
  });
});
