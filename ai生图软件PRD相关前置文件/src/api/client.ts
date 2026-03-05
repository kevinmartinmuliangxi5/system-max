import { validateErrorResponse } from '../contracts/validators';

type ApiPostConfig = {
  headers?: Record<string, string>;
};

type ApiResponse<T> = {
  data: T;
  status: number;
};

const BASE_URL = 'https://api.siliconflow.cn';
const TIMEOUT_MS = Number(process.env.EXPO_PUBLIC_API_TIMEOUT_MS ?? 60000);

function toApiError(
  message: string,
  status?: number,
  data?: unknown,
  code?: string
): Error & { response?: { status?: number; data?: unknown }; code?: string } {
  const err = new Error(message) as Error & {
    response?: { status?: number; data?: unknown };
    code?: string;
  };
  err.response = {
    status,
    data,
  };
  if (code) {
    err.code = code;
  }
  return err;
}

export const api = {
  async post<T>(
    path: string,
    payload: unknown,
    config?: ApiPostConfig
  ): Promise<ApiResponse<T>> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      const res = await fetch(`${BASE_URL}${path}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(config?.headers ?? {}),
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      const data = (await res.json()) as T;
      if (!res.ok) {
        let normalizedErrorData: unknown = data;
        try {
          normalizedErrorData = validateErrorResponse(data);
        } catch {
          // Keep raw response data if it doesn't match known error schema.
        }
        throw toApiError(
          `API request failed with status ${res.status}`,
          res.status,
          normalizedErrorData
        );
      }
      return {
        data,
        status: res.status,
      };
    } catch (error) {
      if ((error as { name?: string })?.name === 'AbortError') {
        throw toApiError(`API request timed out after ${TIMEOUT_MS}ms`, undefined, undefined, 'TIMEOUT');
      }
      throw error;
    } finally {
      clearTimeout(timer);
    }
  },
};
