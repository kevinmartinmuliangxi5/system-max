import { describe, expect, it, vi } from 'vitest';
import { insertReplayLog } from '../../src/db/repositories/replay-logs.repo';

describe('replay retention', () => {
  it('keeps only latest 50 replay logs', async () => {
    const db = { runAsync: vi.fn().mockResolvedValue(undefined) };
    await insertReplayLog(db as never, {
      id: 'rp1',
      requestType: 'image_generation',
      maskedPrompt: 'masked prompt',
      errorCode: '503',
      statusCode: 503,
    });

    expect(db.runAsync).toHaveBeenCalledTimes(2);
    expect(db.runAsync.mock.calls[1][0]).toContain('DELETE FROM replay_logs');
    expect(db.runAsync.mock.calls[1][0]).toContain('LIMIT 50');
  });
});
