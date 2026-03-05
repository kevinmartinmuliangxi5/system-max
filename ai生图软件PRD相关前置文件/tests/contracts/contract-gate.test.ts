import { describe, expect, it } from 'vitest';
import {
  validateErrorResponse,
  validateImageResponse,
  validatePromptEnhanceResponse,
} from '../../src/contracts/validators';

describe('contract gate', () => {
  it('throws when image response shape is invalid', () => {
    expect(() => validateImageResponse({ foo: 1 })).toThrow();
  });

  it('throws when prompt enhance response shape is invalid', () => {
    expect(() => validatePromptEnhanceResponse({ choices: [] })).toThrow();
  });

  it('throws when error response shape is invalid', () => {
    expect(() => validateErrorResponse({ message: 'failed' })).toThrow();
  });
});
