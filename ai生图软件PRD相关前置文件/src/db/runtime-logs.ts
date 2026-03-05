import { insertReplayLog } from './repositories/replay-logs.repo';
import { insertRequestLog } from './repositories/request-logs.repo';
import { getRuntimeDb, runtimeUniqueId } from './runtime-db';

export async function logRequest(params: {
  requestType: 'prompt_enhance' | 'image_generation' | 'image_edit';
  statusCode?: number;
  retryCount?: number;
  durationMs: number;
  costEstimate?: number;
  success: 0 | 1;
  errorCode?: string;
  conversationId?: string;
  messageId?: string;
}) {
  const db = await getRuntimeDb();
  if (!db) {
    return;
  }

  await insertRequestLog(db, {
    id: runtimeUniqueId('req'),
    requestType: params.requestType,
    statusCode: params.statusCode ?? null,
    retryCount: params.retryCount ?? 0,
    durationMs: params.durationMs,
    costEstimate: params.costEstimate ?? 0,
    success: params.success,
    errorCode: params.errorCode ?? null,
    conversationId: params.conversationId ?? null,
    messageId: params.messageId ?? null,
  });
}

export async function logReplay(params: {
  requestType: 'prompt_enhance' | 'image_generation' | 'image_edit';
  maskedPrompt: string;
  errorCode: string;
  statusCode?: number;
}) {
  const db = await getRuntimeDb();
  if (!db) {
    return;
  }

  await insertReplayLog(db, {
    id: runtimeUniqueId('replay'),
    requestType: params.requestType,
    maskedPrompt: params.maskedPrompt,
    errorCode: params.errorCode,
    statusCode: params.statusCode ?? null,
    requestLogId: null,
  });
}
