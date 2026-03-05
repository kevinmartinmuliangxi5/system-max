import { beforeEach, describe, expect, it } from 'vitest';

import {
  clearLatestResult,
  getLatestResult,
  setLatestResult,
} from '../../src/stores/latest-result.store';

describe('latest result store', () => {
  beforeEach(() => {
    clearLatestResult();
  });

  it('stores and reads latest result in memory', () => {
    const saved = setLatestResult({
      imageUri: 'https://example.com/image.png',
      prompt: 'a robot cat',
    });

    expect(saved.imageUri).toBe('https://example.com/image.png');
    expect(saved.prompt).toBe('a robot cat');
    expect(saved.updatedAt).toBeTypeOf('number');

    const read = getLatestResult();
    expect(read).toMatchObject({
      imageUri: 'https://example.com/image.png',
      prompt: 'a robot cat',
    });
  });

  it('clears latest result', () => {
    setLatestResult({
      imageUri: 'https://example.com/image.png',
    });
    clearLatestResult();
    expect(getLatestResult()).toBeNull();
  });
});
