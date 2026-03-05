import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

describe('chat page preview smoke', () => {
  it('contains inline generated image preview element', () => {
    const chatPagePath = path.join(process.cwd(), 'app', 'chat.tsx');
    const source = fs.readFileSync(chatPagePath, 'utf8');

    expect(source).toContain('testID="chat-preview-image"');
    expect(source).toContain('A-ENTERPRISE');
    expect(source).toContain('chat-bottom-pill');
  });
});
