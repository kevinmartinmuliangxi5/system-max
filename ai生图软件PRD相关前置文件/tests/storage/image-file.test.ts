import { describe, expect, it, vi } from 'vitest';

vi.mock('expo-file-system', () => ({
  cacheDirectory: 'file://cache/',
  EncodingType: { Base64: 'base64' },
  writeAsStringAsync: vi.fn().mockResolvedValue(undefined),
}));

import * as FileSystem from 'expo-file-system';
import { persistBase64Image } from '../../src/storage/image-file';

describe('image file', () => {
  it('writes base64 image into file path', async () => {
    const uri = await persistBase64Image('img1', 'ZmFrZQ==');
    expect(uri).toBe('file://cache/img1.png');
    expect(FileSystem.writeAsStringAsync).toHaveBeenCalledWith(
      'file://cache/img1.png',
      'ZmFrZQ==',
      {
        encoding: 'base64',
      }
    );
  });
});
