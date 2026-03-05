import { generateImage } from '../api/images';
import { readStatusCode, retryWithPolicy } from '../api/retry';
import { validateImageResponse } from '../contracts/validators';
import { saveInpaintHistory } from '../db/runtime-history';
import { logReplay, logRequest } from '../db/runtime-logs';
import { persistBase64Image } from '../storage/image-file';

type InpaintDeps = {
  generateImage: typeof generateImage;
  persistBase64Image: typeof persistBase64Image;
  logRequest: typeof logRequest;
  logReplay: typeof logReplay;
  validateImageResponse: typeof validateImageResponse;
  saveInpaintHistory: typeof saveInpaintHistory;
  sleep: (ms: number) => Promise<void>;
};

type InpaintInput = {
  key: string;
  prompt: string;
  imageUri: string;
  maskUri: string;
  conversationId?: string;
  deps?: Partial<InpaintDeps>;
};

type RetryableFailure = {
  retryCount?: number;
  code?: string;
};

function resolveDeps(deps?: Partial<InpaintDeps>): InpaintDeps {
  return {
    generateImage: deps?.generateImage ?? generateImage,
    persistBase64Image: deps?.persistBase64Image ?? persistBase64Image,
    logRequest: deps?.logRequest ?? logRequest,
    logReplay: deps?.logReplay ?? logReplay,
    validateImageResponse: deps?.validateImageResponse ?? validateImageResponse,
    saveInpaintHistory: deps?.saveInpaintHistory ?? saveInpaintHistory,
    sleep: deps?.sleep ?? ((ms: number) => new Promise((resolve) => setTimeout(resolve, ms))),
  };
}

function asRetryCount(error: unknown): number {
  const retryCount = (error as RetryableFailure)?.retryCount;
  return typeof retryCount === 'number' ? retryCount : 0;
}

function estimateCost(input: unknown): number {
  const totalTokens = (input as { usage?: { total_tokens?: number } })?.usage?.total_tokens;
  if (typeof totalTokens === 'number' && totalTokens > 0) {
    return Number((totalTokens * 0.000001).toFixed(6));
  }
  return 0;
}

function createSchemaError(message: string) {
  const error = new Error(message) as Error & { code?: string };
  error.code = 'INVALID_RESPONSE_SCHEMA';
  return error;
}

async function safeLog(task: Promise<unknown>) {
  await Promise.race([
    task.catch(() => undefined),
    new Promise((resolve) => setTimeout(resolve, 800)),
  ]);
}

export async function inpaintImage(input: InpaintInput) {
  const deps = resolveDeps(input.deps);
  const startedAt = Date.now();

  try {
    const imageCall = await retryWithPolicy(
      () =>
        deps.generateImage(input.key, {
          model: 'Qwen/Qwen-Image-Edit',
          prompt: input.prompt,
          image: input.imageUri,
          mask: input.maskUri,
          response_format: 'b64_json',
        }),
      { sleep: deps.sleep }
    );

    const validatedImage = deps.validateImageResponse(imageCall.value.data);
    const imagePayload = validatedImage.data[0];
    const updatedImageUri = imagePayload.b64_json
      ? await deps.persistBase64Image(`inpaint_${Date.now()}`, imagePayload.b64_json)
      : (imagePayload.url ?? '');
    if (!updatedImageUri) {
      throw createSchemaError('Image response is missing b64_json/url payload');
    }

    const history = input.conversationId
      ? await deps.saveInpaintHistory({
          conversationId: input.conversationId,
          userPrompt: input.prompt,
          sourceImageUri: input.imageUri,
          maskUri: input.maskUri,
          imageUri: updatedImageUri,
        })
      : {};

    await safeLog(
      deps.logRequest({
        requestType: 'image_edit',
        durationMs: Date.now() - startedAt,
        success: 1,
        retryCount: imageCall.retryCount,
        conversationId: input.conversationId,
        messageId: history.assistantMessageId,
        costEstimate: estimateCost(imageCall.value.data),
      })
    );

    return {
      status: 'succeeded' as const,
      updatedImageUri,
    };
  } catch (error) {
    const statusCode = readStatusCode(error);
    const errorCode = (error as RetryableFailure)?.code ?? String(statusCode ?? 'UNKNOWN');
    await safeLog(
      deps.logRequest({
        requestType: 'image_edit',
        durationMs: Date.now() - startedAt,
        success: 0,
        statusCode,
        retryCount: asRetryCount(error),
        errorCode,
        conversationId: input.conversationId,
      })
    );
    await safeLog(
      deps.logReplay({
        requestType: 'image_edit',
        maskedPrompt: `${input.prompt.slice(0, 24)}***`,
        errorCode,
        statusCode,
      })
    );
    throw error;
  }
}
