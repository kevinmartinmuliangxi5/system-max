import { insertMessage } from './repositories/messages.repo';
import { getRuntimeDb, runtimeUniqueId } from './runtime-db';

type SaveConversationHistoryInput = {
  conversationId: string;
  userPrompt: string;
  assistantPrompt: string;
  imageUri: string;
};

type SaveInpaintHistoryInput = {
  conversationId: string;
  userPrompt: string;
  sourceImageUri: string;
  maskUri: string;
  imageUri: string;
};

type SaveHistoryResult = {
  assistantMessageId?: string;
};

type MessageInsertInput = Parameters<typeof insertMessage>[1];

async function ensureConversation(conversationId: string, title: string) {
  const db = await getRuntimeDb();
  if (!db) {
    return null;
  }

  const now = Date.now();
  await db.runAsync(
    'INSERT OR IGNORE INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)',
    conversationId,
    title,
    now,
    now
  );
  await db.runAsync(
    'UPDATE conversations SET updated_at = ? WHERE id = ?',
    now,
    conversationId
  );
  return db;
}

function isLegacyImageUriConstraintError(error: unknown): boolean {
  const message = (error as { message?: string })?.message;
  return (
    typeof message === 'string' &&
    /CHECK constraint failed:\s*image_uri/i.test(message)
  );
}

async function insertMessageWithLegacyUriFallback(
  db: NonNullable<Awaited<ReturnType<typeof getRuntimeDb>>>,
  message: MessageInsertInput
) {
  try {
    await insertMessage(db, message);
  } catch (error) {
    const canFallback =
      isLegacyImageUriConstraintError(error) &&
      typeof message.imageUri === 'string' &&
      /^https?:\/\//i.test(message.imageUri);
    if (!canFallback) {
      throw error;
    }

    await insertMessage(db, {
      ...message,
      imageUri: null,
    });
  }
}

export async function saveConversationHistory(
  input: SaveConversationHistoryInput
): Promise<SaveHistoryResult> {
  const db = await ensureConversation(
    input.conversationId,
    input.userPrompt.slice(0, 48) || 'Untitled Conversation'
  );
  if (!db) {
    return {};
  }

  const userMessageId = runtimeUniqueId('msg_user');
  const assistantMessageId = runtimeUniqueId('msg_assistant');

  await insertMessage(db, {
    id: userMessageId,
    conversationId: input.conversationId,
    role: 'user',
    text: input.userPrompt,
    imageUri: null,
    maskUri: null,
    status: 'succeeded',
  });

  await insertMessageWithLegacyUriFallback(db, {
    id: assistantMessageId,
    conversationId: input.conversationId,
    role: 'assistant',
    text: input.assistantPrompt,
    imageUri: input.imageUri,
    maskUri: null,
    status: 'succeeded',
  });

  return { assistantMessageId };
}

export async function saveInpaintHistory(
  input: SaveInpaintHistoryInput
): Promise<SaveHistoryResult> {
  const db = await ensureConversation(
    input.conversationId,
    input.userPrompt.slice(0, 48) || 'Untitled Conversation'
  );
  if (!db) {
    return {};
  }

  const userMessageId = runtimeUniqueId('msg_user');
  const assistantMessageId = runtimeUniqueId('msg_assistant');

  await insertMessageWithLegacyUriFallback(db, {
    id: userMessageId,
    conversationId: input.conversationId,
    role: 'user',
    text: input.userPrompt,
    imageUri: input.sourceImageUri,
    maskUri: input.maskUri,
    status: 'succeeded',
  });

  await insertMessageWithLegacyUriFallback(db, {
    id: assistantMessageId,
    conversationId: input.conversationId,
    role: 'assistant',
    text: input.userPrompt,
    imageUri: input.imageUri,
    maskUri: input.maskUri,
    status: 'succeeded',
  });

  return { assistantMessageId };
}
