import { describe, expect, it, vi } from 'vitest';
import { runInitialMigration } from '../../src/db/migrate';

describe('db migrate', () => {
  it('executes initial sql migration', async () => {
    const db = { execAsync: vi.fn().mockResolvedValue(undefined) };
    await runInitialMigration(db as never);
    expect(db.execAsync).toHaveBeenCalledTimes(1);
    expect(db.execAsync.mock.calls[0][0]).toContain('CREATE TABLE IF NOT EXISTS conversations');
  });
});
