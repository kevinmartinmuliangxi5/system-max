import { describe, expect, it } from 'vitest';

import { exportWithAigcMeta } from '../../src/export/aigc-export';

describe('aigc export', () => {
  it('returns uri with aigc watermark info', async () => {
    const result = await exportWithAigcMeta('file://image.png');
    expect(result).toEqual({
      uri: 'file://image.png',
      watermark: 'AI生成/AIGC',
    });
  });
});
