type MessageInsert = {
  id: string;
  conversationId: string;
  role: 'system' | 'user' | 'assistant';
  text: string | null;
  imageUri: string | null;
  maskUri: string | null;
  status: 'pending' | 'running' | 'succeeded' | 'failed' | 'cancelled';
};

export async function insertMessage(
  db: { runAsync: (sql: string, ...params: unknown[]) => Promise<unknown> },
  message: MessageInsert
) {
  const now = Date.now();
  return db.runAsync(
    `INSERT INTO messages (
      id, conversation_id, role, text, image_uri, mask_uri, status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    message.id,
    message.conversationId,
    message.role,
    message.text,
    message.imageUri,
    message.maskUri,
    message.status,
    now,
    now
  );
}
