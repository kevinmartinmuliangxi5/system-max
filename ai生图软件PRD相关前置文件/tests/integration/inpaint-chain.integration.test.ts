import { describe, expect, it, vi } from 'vitest';

vi.mock('expo-file-system', () => ({
  cacheDirectory: 'file://cache/',
  EncodingType: { Base64: 'base64' },
  writeAsStringAsync: vi.fn().mockResolvedValue(undefined),
}));

import * as FileSystem from 'expo-file-system';
import { api } from '../../src/api/client';
import { inpaintImage } from '../../src/flows/inpaint-image';

describe('inpaint integration chain', () => {
  it('runs image generation with mask and persists updated image', async () => {
    const postSpy = vi.spyOn(api, 'post').mockResolvedValue({
      data: { data: [{ b64_json: 'dXBkYXRlZA==' }] },
    } as never);

    const result = await inpaintImage({
      key: 'sk-key',
      prompt: 'replace object',
      imageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
    });

    expect(postSpy).toHaveBeenCalledWith(
      '/v1/images/generations',
      {
        model: 'Qwen/Qwen-Image-Edit',
        prompt: 'replace object',
        image: 'file://origin.png',
        mask: 'file://mask.png',
        response_format: 'b64_json',
      },
      { headers: { Authorization: 'Bearer sk-key' } }
    );
    expect(FileSystem.writeAsStringAsync).toHaveBeenCalledWith(
      expect.stringMatching(/^file:\/\/cache\/inpaint_\d+\.png$/),
      'dXBkYXRlZA==',
      { encoding: 'base64' }
    );
    expect(result.status).toBe('succeeded');
    expect(result.updatedImageUri).toMatch(/^file:\/\/cache\/inpaint_\d+\.png$/);
  });
});
