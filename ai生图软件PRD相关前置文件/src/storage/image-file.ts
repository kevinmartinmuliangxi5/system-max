import * as FileSystem from 'expo-file-system';

export async function persistBase64Image(
  id: string,
  base64: string
): Promise<string> {
  const uri = `${FileSystem.cacheDirectory}${id}.png`;
  await FileSystem.writeAsStringAsync(uri, base64, {
    encoding: FileSystem.EncodingType.Base64,
  });
  return uri;
}
