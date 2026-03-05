export function maskKey(key: string): string {
  if (key.length <= 5) {
    return '***';
  }
  return `${key.slice(0, 3)}***${key.slice(-2)}`;
}
