import { describe, expect, it } from 'vitest';

import { runInitialMigration } from '../../src/db/migrate';
import { createConversation } from '../../src/db/repositories/conversations.repo';
import { insertMessage } from '../../src/db/repositories/messages.repo';
import { insertRequestLog } from '../../src/db/repositories/request-logs.repo';
import { createSqlJsTestDb } from './helpers/sqljs-test-db';

describe('db integration: migration + repositories', () => {
  it('creates tables and persists conversation/message/request log chain', async () => {
    const db = await createSqlJsTestDb();
    await runInitialMigration(db.asyncDb);

    await createConversation(db.asyncDb, 'c1', 'first chat');
    await insertMessage(db.asyncDb, {
      id: 'm1',
      conversationId: 'c1',
      role: 'user',
      text: 'hello',
      imageUri: null,
      maskUri: null,
      status: 'pending',
    });
    await insertRequestLog(db.asyncDb, {
      id: 'r1',
      conversationId: 'c1',
      messageId: 'm1',
      requestType: 'image_generation',
      statusCode: 200,
      retryCount: 0,
      durationMs: 100,
      costEstimate: 0.01,
      success: 1,
      errorCode: null,
    });

    expect(db.scalar('SELECT COUNT(*) FROM conversations')).toBe(1);
    expect(db.scalar('SELECT COUNT(*) FROM messages')).toBe(1);
    expect(db.scalar('SELECT COUNT(*) FROM request_logs')).toBe(1);
    expect(
      db.scalar(
        "SELECT COUNT(*) FROM request_logs WHERE conversation_id = 'c1' AND message_id = 'm1'"
      )
    ).toBe(1);
  });

  it('accepts remote image url in message history', async () => {
    const db = await createSqlJsTestDb();
    await runInitialMigration(db.asyncDb);

    await createConversation(db.asyncDb, 'c2', 'remote image chat');
    await insertMessage(db.asyncDb, {
      id: 'm2',
      conversationId: 'c2',
      role: 'assistant',
      text: null,
      imageUri: 'https://example.com/generated.png',
      maskUri: null,
      status: 'succeeded',
    });

    expect(db.scalar("SELECT COUNT(*) FROM messages WHERE id = 'm2'")).toBe(1);
    expect(
      db.text("SELECT image_uri FROM messages WHERE id = 'm2'")
    ).toBe('https://example.com/generated.png');
  });
});
