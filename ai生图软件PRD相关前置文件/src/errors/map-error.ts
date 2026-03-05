type ErrorInput = {
  status?: number;
  code?: string;
};

export function mapErrorMessage(input: ErrorInput): string {
  if (input.code === 'TIMEOUT') {
    return 'Request timed out after retries. Please try again.';
  }
  if (input.code === 'INVALID_RESPONSE_SCHEMA') {
    return 'Image response format is unsupported. Please retry or switch model.';
  }
  if (input.status === 429) {
    return 'Too many requests, retrying automatically.';
  }
  if (input.status === 503) {
    return 'Service temporarily unavailable, please retry.';
  }
  if (typeof input.status === 'number' && input.status >= 400 && input.status < 500) {
    return 'Request rejected. Please check your input and API key.';
  }
  return 'Request failed, please retry.';
}
