type RetryableError = {
  response?: { status?: number };
  code?: string;
  message?: string;
  retryCount?: number;
};

type RetryOptions = {
  maxStatusRetries?: number;
  maxTimeoutRetries?: number;
  baseDelayMs?: number;
  sleep?: (ms: number) => Promise<void>;
  onRetry?: (context: {
    retryCount: number;
    reason: 'status' | 'timeout';
    status?: number;
    delayMs: number;
  }) => void;
};

type RetryResult<T> = {
  value: T;
  retryCount: number;
};

const DEFAULT_BASE_DELAY_MS = Number(
  process.env.EXPO_PUBLIC_RETRY_BASE_DELAY_MS ?? 300
);

export const MAX_STATUS_RETRIES = 3;
export const MAX_TIMEOUT_RETRIES = 2;

function sleepDefault(ms: number) {
  return new Promise<void>((resolve) => setTimeout(resolve, ms));
}

export function shouldRetry(status?: number): boolean {
  return status === 429 || status === 503;
}

export function readStatusCode(error: unknown): number | undefined {
  const status = (error as RetryableError)?.response?.status;
  return typeof status === 'number' ? status : undefined;
}

export function isTimeoutError(error: unknown): boolean {
  const code = (error as RetryableError)?.code;
  if (code === 'TIMEOUT') {
    return true;
  }

  const message = (error as RetryableError)?.message ?? '';
  return /timed out/i.test(message);
}

export function nextDelayMs(retryIndex: number, baseDelayMs = DEFAULT_BASE_DELAY_MS): number {
  return baseDelayMs * 2 ** retryIndex;
}

export async function retryWithPolicy<T>(
  task: () => Promise<T>,
  options?: RetryOptions
): Promise<RetryResult<T>> {
  const maxStatusRetries = options?.maxStatusRetries ?? MAX_STATUS_RETRIES;
  const maxTimeoutRetries = options?.maxTimeoutRetries ?? MAX_TIMEOUT_RETRIES;
  const baseDelayMs = options?.baseDelayMs ?? DEFAULT_BASE_DELAY_MS;
  const sleep = options?.sleep ?? sleepDefault;

  let retryCount = 0;
  let statusRetryCount = 0;
  let timeoutRetryCount = 0;

  for (;;) {
    try {
      const value = await task();
      return { value, retryCount };
    } catch (error) {
      const status = readStatusCode(error);
      if (shouldRetry(status) && statusRetryCount < maxStatusRetries) {
        const delayMs = nextDelayMs(statusRetryCount, baseDelayMs);
        statusRetryCount += 1;
        retryCount += 1;
        options?.onRetry?.({ retryCount, reason: 'status', status, delayMs });
        await sleep(delayMs);
        continue;
      }

      if (isTimeoutError(error) && timeoutRetryCount < maxTimeoutRetries) {
        const delayMs = nextDelayMs(timeoutRetryCount, baseDelayMs);
        timeoutRetryCount += 1;
        retryCount += 1;
        options?.onRetry?.({ retryCount, reason: 'timeout', delayMs });
        await sleep(delayMs);
        continue;
      }

      const retryableError = error as RetryableError;
      retryableError.retryCount = retryCount;
      throw retryableError;
    }
  }
}
