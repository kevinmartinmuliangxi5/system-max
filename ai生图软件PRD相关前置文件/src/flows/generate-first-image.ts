import { generateImage } from '../api/images';
import { readStatusCode, retryWithPolicy } from '../api/retry';
import { enhancePrompt } from '../api/prompt';
import {
  validateImageResponse,
  validatePromptEnhanceResponse,
} from '../contracts/validators';
import { saveConversationHistory } from '../db/runtime-history';
import { logReplay, logRequest } from '../db/runtime-logs';
import { persistBase64Image } from '../storage/image-file';

type FirstImageDeps = {
  enhancePrompt: typeof enhancePrompt;
  generateImage: typeof generateImage;
  persistBase64Image: typeof persistBase64Image;
  logRequest: typeof logRequest;
  logReplay: typeof logReplay;
  validatePromptEnhanceResponse: typeof validatePromptEnhanceResponse;
  validateImageResponse: typeof validateImageResponse;
  saveConversationHistory: typeof saveConversationHistory;
  sleep: (ms: number) => Promise<void>;
};

type FirstImageInput = {
  prompt: string;
  key: string;
  conversationId: string;
  deps?: Partial<FirstImageDeps>;
};

type RetryableFailure = {
  response?: { status?: number };
  retryCount?: number;
  code?: string;
};

function resolveDeps(deps?: Partial<FirstImageDeps>): FirstImageDeps {
  return {
    enhancePrompt: deps?.enhancePrompt ?? enhancePrompt,
    generateImage: deps?.generateImage ?? generateImage,
    persistBase64Image: deps?.persistBase64Image ?? persistBase64Image,
    logRequest: deps?.logRequest ?? logRequest,
    logReplay: deps?.logReplay ?? logReplay,
    validatePromptEnhanceResponse:
      deps?.validatePromptEnhanceResponse ?? validatePromptEnhanceResponse,
    validateImageResponse: deps?.validateImageResponse ?? validateImageResponse,
    saveConversationHistory: deps?.saveConversationHistory ?? saveConversationHistory,
    sleep: deps?.sleep ?? ((ms: number) => new Promise((resolve) => setTimeout(resolve, ms))),
  };
}

function asRetryCount(error: unknown): number {
  const retryCount = (error as RetryableFailure)?.retryCount;
  return typeof retryCount === 'number' ? retryCount : 0;
}

function resolveEnhancedPrompt(
  inputPrompt: string,
  payload: unknown,
  validate: typeof validatePromptEnhanceResponse
): string {
  try {
    const validated = validate(payload);
    const value = validated.choices[0]?.message?.content?.trim();
    return value || inputPrompt;
  } catch {
    return inputPrompt;
  }
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

export async function generateFirstImage(input: FirstImageInput) {
  const deps = resolveDeps(input.deps);
  const startedAt = Date.now();
  let failedRequestType: 'prompt_enhance' | 'image_generation' = 'prompt_enhance';

  try {
    const promptCall = await retryWithPolicy(
      () =>
        deps.enhancePrompt(input.key, {
          model: 'deepseek-ai/DeepSeek-V3',
          messages: [{ role: 'user', content: input.prompt }],
        }),
      { sleep: deps.sleep }
    );

    const enhancedPrompt = resolveEnhancedPrompt(
      input.prompt,
      promptCall.value.data,
      deps.validatePromptEnhanceResponse
    );

    await safeLog(
      deps.logRequest({
        requestType: 'prompt_enhance',
        durationMs: Date.now() - startedAt,
        success: 1,
        retryCount: promptCall.retryCount,
        conversationId: input.conversationId,
        costEstimate: estimateCost(promptCall.value.data),
      })
    );

    failedRequestType = 'image_generation';
    const imageCall = await retryWithPolicy(
      () =>
        deps.generateImage(input.key, {
          model: 'black-forest-labs/FLUX.1-schnell',
          prompt: enhancedPrompt,
          response_format: 'b64_json',
        }),
      { sleep: deps.sleep }
    );

    const validatedImage = deps.validateImageResponse(imageCall.value.data);
    const imagePayload = validatedImage.data[0];
    const imageUri = imagePayload.b64_json
      ? await deps.persistBase64Image(`gen_${Date.now()}`, imagePayload.b64_json)
      : (imagePayload.url ?? '');
    if (!imageUri) {
      throw createSchemaError('Image response is missing b64_json/url payload');
    }
    const history = await deps.saveConversationHistory({
      conversationId: input.conversationId,
      userPrompt: input.prompt,
      assistantPrompt: enhancedPrompt,
      imageUri,
    });

    await safeLog(
      deps.logRequest({
        requestType: 'image_generation',
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
      imageUri,
      prompt: enhancedPrompt,
      conversationId: input.conversationId,
    };
  } catch (error) {
    const statusCode = readStatusCode(error);
    const errorCode = (error as RetryableFailure)?.code ?? String(statusCode ?? 'UNKNOWN');
    await safeLog(
      deps.logRequest({
        requestType: failedRequestType,
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
        requestType: failedRequestType,
        maskedPrompt: `${input.prompt.slice(0, 24)}***`,
        errorCode,
        statusCode,
      })
    );
    throw error;
  }
}
