import { describe, expect, it } from 'vitest';

import { runInitialMigration } from '../../src/db/migrate';
import { insertReplayLog } from '../../src/db/repositories/replay-logs.repo';
import { createSqlJsTestDb } from './helpers/sqljs-test-db';

describe('db integration: replay retention', () => {
  it('keeps only latest 50 replay logs after many inserts', async () => {
    const db = await createSqlJsTestDb();
    await runInitialMigration(db.asyncDb);

    for (let i = 1; i <= 60; i += 1) {
      await insertReplayLog(db.asyncDb, {
        id: `rp-${i}`,
        requestType: 'image_generation',
        maskedPrompt: `prompt-${i}`,
        errorCode: '503',
        statusCode: 503,
      });
    }

    expect(db.scalar('SELECT COUNT(*) FROM replay_logs')).toBe(50);
    expect(
      db.scalar("SELECT COUNT(*) FROM replay_logs WHERE id = 'rp-1'")
    ).toBe(0);
    expect(
      db.scalar("SELECT COUNT(*) FROM replay_logs WHERE id = 'rp-60'")
    ).toBe(1);
  });
});

