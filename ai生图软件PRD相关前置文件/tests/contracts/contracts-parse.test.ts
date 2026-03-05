import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const files = [
  'contracts/prompt-enhance.response.schema.json',
  'contracts/image-generation.response.schema.json',
  'contracts/error.schema.json',
];

describe('contracts parse', () => {
  it('loads all schema files as valid json', () => {
    for (const file of files) {
      const raw = fs.readFileSync(path.join(root, file), 'utf8');
      expect(() => JSON.parse(raw)).not.toThrow();
    }
  });
});
