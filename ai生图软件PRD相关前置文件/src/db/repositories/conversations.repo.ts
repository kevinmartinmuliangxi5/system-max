export async function createConversation(
  db: { runAsync: (sql: string, ...params: unknown[]) => Promise<unknown> },
  id: string,
  title: string
) {
  const now = Date.now();
  return db.runAsync(
    'INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)',
    id,
    title,
    now,
    now
  );
}
