type ReplayLogInsert = {
  id: string;
  requestLogId?: string | null;
  requestType: 'prompt_enhance' | 'image_generation' | 'image_edit';
  maskedPrompt: string;
  errorCode: string;
  statusCode?: number | null;
};

async function pruneReplayLogs(
  db: { runAsync: (sql: string, ...params: unknown[]) => Promise<unknown> }
) {
  return db.runAsync(
    'DELETE FROM replay_logs WHERE id NOT IN (SELECT id FROM replay_logs ORDER BY created_at DESC LIMIT 50)'
  );
}

export async function insertReplayLog(
  db: { runAsync: (sql: string, ...params: unknown[]) => Promise<unknown> },
  log: ReplayLogInsert
) {
  const now = Date.now();
  await db.runAsync(
    `INSERT INTO replay_logs (
      id, request_log_id, request_type, masked_prompt, error_code, status_code, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)`,
    log.id,
    log.requestLogId ?? null,
    log.requestType,
    log.maskedPrompt,
    log.errorCode,
    log.statusCode ?? null,
    now
  );
  await pruneReplayLogs(db);
}
