import { describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  runAsync: vi.fn().mockResolvedValue(undefined),
}));

vi.mock('../../src/db/runtime-db', () => {
  let id = 0;
  return {
    getRuntimeDb: vi.fn().mockResolvedValue({
      runAsync: mocks.runAsync,
      execAsync: vi.fn().mockResolvedValue(undefined),
    }),
    runtimeUniqueId: vi.fn((prefix: string) => {
      id += 1;
      return `${prefix}_${id}`;
    }),
  };
});

import {
  saveConversationHistory,
  saveInpaintHistory,
} from '../../src/db/runtime-history';

describe('runtime history', () => {
  it('persists conversation + user + assistant messages for first image', async () => {
    mocks.runAsync.mockClear();

    const result = await saveConversationHistory({
      conversationId: 'c1',
      userPrompt: 'draw city skyline',
      assistantPrompt: 'enhanced city skyline',
      imageUri: 'file://img.png',
    });

    expect(result.assistantMessageId).toBe('msg_assistant_2');
    expect(
      mocks.runAsync.mock.calls.some((c) =>
        String(c[0]).includes('INSERT OR IGNORE INTO conversations')
      )
    ).toBe(true);
    expect(
      mocks.runAsync.mock.calls.some((c) =>
        String(c[0]).includes('UPDATE conversations SET updated_at')
      )
    ).toBe(true);
    expect(
      mocks.runAsync.mock.calls.filter((c) =>
        String(c[0]).includes('INSERT INTO messages')
      ).length
    ).toBe(2);
  });

  it('persists inpaint history with source image and mask linkage', async () => {
    mocks.runAsync.mockClear();

    const result = await saveInpaintHistory({
      conversationId: 'c1',
      userPrompt: 'replace sky',
      sourceImageUri: 'file://origin.png',
      maskUri: 'file://mask.png',
      imageUri: 'file://updated.png',
    });

    expect(result.assistantMessageId).toBe('msg_assistant_4');
    expect(
      mocks.runAsync.mock.calls.filter((c) =>
        String(c[0]).includes('INSERT INTO messages')
      ).length
    ).toBe(2);
  });

  it('falls back when legacy image_uri constraint rejects remote url', async () => {
    mocks.runAsync.mockClear();
    mocks.runAsync.mockImplementation(async (sql: string, ...params: unknown[]) => {
      if (
        String(sql).includes('INSERT INTO messages') &&
        params.includes('https://example.com/generated.png')
      ) {
        throw new Error("CHECK constraint failed: image_uri IS NULL OR image_uri LIKE 'file://%'");
      }
      return undefined;
    });

    const result = await saveConversationHistory({
      conversationId: 'c3',
      userPrompt: 'draw cat',
      assistantPrompt: 'enhanced cat',
      imageUri: 'https://example.com/generated.png',
    });

    expect(result.assistantMessageId).toBe('msg_assistant_6');
    const messageInserts = mocks.runAsync.mock.calls.filter((c) =>
      String(c[0]).includes('INSERT INTO messages')
    );
    expect(messageInserts.length).toBe(3);
    expect(
      messageInserts.some((call) => call[3] === 'assistant' && call[5] === null)
    ).toBe(true);
  });
});
