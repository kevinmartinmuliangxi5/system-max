import { describe, expect, it } from 'vitest';

import { mapErrorMessage } from '../../src/errors/map-error';

describe('map error', () => {
  it('maps 429 status to retry hint', () => {
    expect(mapErrorMessage({ status: 429 })).toBe(
      'Too many requests, retrying automatically.'
    );
  });

  it('maps timeout code to timeout hint', () => {
    expect(mapErrorMessage({ code: 'TIMEOUT' })).toBe(
      'Request timed out after retries. Please try again.'
    );
  });

  it('maps schema error code to response format guidance', () => {
    expect(mapErrorMessage({ code: 'INVALID_RESPONSE_SCHEMA' })).toBe(
      'Image response format is unsupported. Please retry or switch model.'
    );
  });

  it('maps non-retriable 4xx to input guidance', () => {
    expect(mapErrorMessage({ status: 401 })).toBe(
      'Request rejected. Please check your input and API key.'
    );
  });
});
