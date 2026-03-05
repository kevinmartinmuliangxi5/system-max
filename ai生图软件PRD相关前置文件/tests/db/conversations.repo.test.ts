import { describe, expect, it, vi } from 'vitest';
import { createConversation } from '../../src/db/repositories/conversations.repo';

describe('conversations repo', () => {
  it('inserts a conversation row', async () => {
    const db = { runAsync: vi.fn().mockResolvedValue(undefined) };
    await createConversation(db as never, 'c1', 'First Chat');
    expect(db.runAsync).toHaveBeenCalledTimes(1);
    expect(db.runAsync.mock.calls[0][0]).toContain('INSERT INTO conversations');
    expect(db.runAsync.mock.calls[0][1]).toBe('c1');
  });
});
