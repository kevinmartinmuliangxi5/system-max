import { describe, expect, it, vi } from 'vitest';
import {
  nextDelayMs,
  retryWithPolicy,
  shouldRetry,
} from '../../src/api/retry';

describe('retry policy', () => {
  it('retries for 429 and 503 only', () => {
    expect(shouldRetry(429)).toBe(true);
    expect(shouldRetry(503)).toBe(true);
    expect(shouldRetry(400)).toBe(false);
    expect(shouldRetry(undefined)).toBe(false);
  });

  it('uses exponential backoff delays', () => {
    expect(nextDelayMs(0, 100)).toBe(100);
    expect(nextDelayMs(1, 100)).toBe(200);
    expect(nextDelayMs(2, 100)).toBe(400);
  });

  it('retries 429/503 and returns retry count', async () => {
    const sleep = vi.fn().mockResolvedValue(undefined);
    const task = vi
      .fn()
      .mockRejectedValueOnce({ response: { status: 429 } })
      .mockRejectedValueOnce({ response: { status: 503 } })
      .mockResolvedValueOnce('ok');

    const result = await retryWithPolicy(task, {
      sleep,
      baseDelayMs: 1,
    });

    expect(result.value).toBe('ok');
    expect(result.retryCount).toBe(2);
    expect(task).toHaveBeenCalledTimes(3);
    expect(sleep).toHaveBeenCalledTimes(2);
  });

  it('retries timeout errors up to configured limit', async () => {
    const sleep = vi.fn().mockResolvedValue(undefined);
    const timeoutErr = { code: 'TIMEOUT' };
    const task = vi
      .fn()
      .mockRejectedValueOnce(timeoutErr)
      .mockRejectedValueOnce(timeoutErr)
      .mockResolvedValueOnce('ok');

    const result = await retryWithPolicy(task, {
      sleep,
      baseDelayMs: 1,
    });

    expect(result.value).toBe('ok');
    expect(result.retryCount).toBe(2);
    expect(task).toHaveBeenCalledTimes(3);
    expect(sleep).toHaveBeenCalledTimes(2);
  });
});
