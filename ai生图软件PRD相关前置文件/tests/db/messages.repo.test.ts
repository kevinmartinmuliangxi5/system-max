import { describe, expect, it, vi } from 'vitest';
import { insertMessage } from '../../src/db/repositories/messages.repo';

describe('messages repo', () => {
  it('inserts message with conversation_id', async () => {
    const db = { runAsync: vi.fn().mockResolvedValue(undefined) };
    await insertMessage(db as never, {
      id: 'm1',
      conversationId: 'c1',
      role: 'user',
      text: 'hello',
      status: 'pending',
      imageUri: null,
      maskUri: null,
    });
    expect(db.runAsync).toHaveBeenCalledTimes(1);
    expect(db.runAsync.mock.calls[0][0]).toContain('INSERT INTO messages');
    expect(db.runAsync.mock.calls[0][2]).toBe('c1');
  });
});
