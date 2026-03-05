import { describe, expect, it } from 'vitest';

import { maskKey } from '../../src/logging/redact';

describe('redact', () => {
  it('masks api key middle part', () => {
    expect(maskKey('sk-1234567890')).toBe('sk-***90');
  });
});
