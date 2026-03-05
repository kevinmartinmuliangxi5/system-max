import * as FileSystem from 'expo-file-system';

export async function saveMask(uri: string, data: string): Promise<void> {
  await FileSystem.writeAsStringAsync(uri, data);
}
