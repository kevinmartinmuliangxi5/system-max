import { describe, expect, it, vi } from 'vitest';

vi.mock('../../src/api/images', () => ({ generateImage: vi.fn() }));
vi.mock('../../src/storage/image-file', () => ({ persistBase64Image: vi.fn() }));

import { inpaintImage } from '../../src/flows/inpaint-image';

type InpaintDeps = NonNullable<Parameters<typeof inpaintImage>[0]['deps']>;

describe('inpaintImage unit', () => {
  it('sends image+mask payload and writes returned base64', async () => {
    const deps: InpaintDeps = {
      generateImage: vi.fn().mockResolvedValue({ data: { data: [{ b64_json: 'YmFzZTY0' }] } }),
      persistBase64Image: vi.fn().mockResolvedValue('file://updated.png'),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveInpaintHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-inpaint-1' }),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await inpaintImage({
      key: 'sk-demo',
      prompt: 'replace sky',
      imageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
      conversationId: 'c1',
      deps,
    });

    expect(deps.generateImage).toHaveBeenCalledWith('sk-demo', {
      model: 'Qwen/Qwen-Image-Edit',
      prompt: 'replace sky',
      image: 'file://origin.png',
      mask: 'file://mask.png',
      response_format: 'b64_json',
    });
    expect(deps.persistBase64Image).toHaveBeenCalledWith(
      expect.stringMatching(/^inpaint_/),
      'YmFzZTY0'
    );
    expect(deps.saveInpaintHistory).toHaveBeenCalledWith(
      expect.objectContaining({
        conversationId: 'c1',
        userPrompt: 'replace sky',
        sourceImageUri: 'file://origin.png',
        maskUri: 'file://mask.png',
        imageUri: 'file://updated.png',
      })
    );
    expect(deps.logRequest).toHaveBeenCalledWith(
      expect.objectContaining({
        requestType: 'image_edit',
        success: 1,
        conversationId: 'c1',
        messageId: 'm-inpaint-1',
      })
    );
    expect(result.updatedImageUri).toBe('file://updated.png');
  });

  it('retries retriable status codes and logs retry count', async () => {
    const deps: InpaintDeps = {
      generateImage: vi
        .fn()
        .mockRejectedValueOnce({ response: { status: 429 } })
        .mockResolvedValueOnce({ data: { data: [{ b64_json: 'YmFzZTY0' }] } }),
      persistBase64Image: vi.fn().mockResolvedValue('file://updated.png'),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ b64_json: string }> }),
      saveInpaintHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-inpaint-2' }),
      sleep: vi.fn().mockResolvedValue(undefined),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await inpaintImage({
      key: 'sk-demo',
      prompt: 'replace sky',
      imageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
      conversationId: 'c1',
      deps,
    });

    expect(result.status).toBe('succeeded');
    expect(deps.generateImage).toHaveBeenCalledTimes(2);
    expect(deps.logRequest).toHaveBeenCalledWith(
      expect.objectContaining({
        requestType: 'image_edit',
        success: 1,
        retryCount: 1,
      })
    );
  });

  it('rejects when image response fails schema validation', async () => {
    const deps: InpaintDeps = {
      generateImage: vi
        .fn()
        .mockResolvedValue({ data: { data: [{ url: 'https://example.com/updated.png' }] } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn(() => {
        throw new Error('Invalid image response schema');
      }),
      saveInpaintHistory: vi.fn(),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    await expect(
      inpaintImage({
        key: 'sk-demo',
        prompt: 'replace sky',
        imageUri: 'file://origin.png',
        maskUri: 'file://mask.png',
        conversationId: 'c1',
        deps,
      })
    ).rejects.toThrow('Invalid image response schema');

    expect(deps.validateImageResponse).toHaveBeenCalledTimes(1);
    expect(deps.persistBase64Image).not.toHaveBeenCalled();
  });

  it('uses direct image URL when provider returns url', async () => {
    const deps: InpaintDeps = {
      generateImage: vi
        .fn()
        .mockResolvedValue({ data: { data: [{ url: 'https://example.com/updated.png' }] } }),
      persistBase64Image: vi.fn(),
      validateImageResponse: vi.fn((input: unknown) => input as { data: Array<{ url: string }> }),
      saveInpaintHistory: vi.fn().mockResolvedValue({ assistantMessageId: 'm-inpaint-3' }),
      logRequest: vi.fn().mockResolvedValue(undefined),
      logReplay: vi.fn().mockResolvedValue(undefined),
    };

    const result = await inpaintImage({
      key: 'sk-demo',
      prompt: 'replace sky',
      imageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
      conversationId: 'c1',
      deps,
    });

    expect(result.updatedImageUri).toBe('https://example.com/updated.png');
    expect(deps.persistBase64Image).not.toHaveBeenCalled();
  });
});
