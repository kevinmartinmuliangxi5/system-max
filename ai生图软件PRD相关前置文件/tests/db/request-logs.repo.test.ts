import { describe, expect, it, vi } from 'vitest';
import { insertRequestLog } from '../../src/db/repositories/request-logs.repo';

describe('request logs repo', () => {
  it('inserts request log row', async () => {
    const db = { runAsync: vi.fn().mockResolvedValue(undefined) };
    await insertRequestLog(db as never, {
      id: 'r1',
      requestType: 'image_generation',
      statusCode: 200,
      retryCount: 0,
      durationMs: 6201,
      costEstimate: 0.017,
      success: 1,
    });
    expect(db.runAsync).toHaveBeenCalledTimes(1);
    expect(db.runAsync.mock.calls[0][0]).toContain('INSERT INTO request_logs');
  });
});
