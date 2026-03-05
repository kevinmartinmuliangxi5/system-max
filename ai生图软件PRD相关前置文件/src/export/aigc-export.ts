export async function exportWithAigcMeta(uri: string) {
  return {
    uri,
    watermark: 'AI生成/AIGC',
  };
}
