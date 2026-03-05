type RequestLogInsert = {
  id: string;
  conversationId?: string | null;
  messageId?: string | null;
  requestType: 'prompt_enhance' | 'image_generation' | 'image_edit';
  statusCode?: number | null;
  retryCount: number;
  durationMs: number;
  costEstimate: number;
  success: 0 | 1;
  errorCode?: string | null;
};

export async function insertRequestLog(
  db: { runAsync: (sql: string, ...params: unknown[]) => Promise<unknown> },
  log: RequestLogInsert
) {
  const now = Date.now();
  return db.runAsync(
    `INSERT INTO request_logs (
      id, conversation_id, message_id, request_type, provider, status_code,
      retry_count, duration_ms, cost_estimate, success, error_code, created_at
    ) VALUES (?, ?, ?, ?, 'siliconflow', ?, ?, ?, ?, ?, ?, ?)`,
    log.id,
    log.conversationId ?? null,
    log.messageId ?? null,
    log.requestType,
    log.statusCode ?? null,
    log.retryCount,
    log.durationMs,
    log.costEstimate,
    log.success,
    log.errorCode ?? null,
    now
  );
}
