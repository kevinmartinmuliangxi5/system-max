import { describe, expect, it, vi } from 'vitest';

vi.mock('expo-file-system', () => ({
  writeAsStringAsync: vi.fn().mockResolvedValue(undefined),
}));

import * as FileSystem from 'expo-file-system';
import { saveMask } from '../../src/storage/mask-file';

describe('mask file', () => {
  it('writes mask content to uri', async () => {
    await saveMask('file://mask.png', 'base64mask');

    expect(FileSystem.writeAsStringAsync).toHaveBeenCalledWith(
      'file://mask.png',
      'base64mask'
    );
  });
});
