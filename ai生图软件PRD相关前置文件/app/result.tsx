import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { Button, Image, SafeAreaView, ScrollView, Text, View } from 'react-native';

import { exportWithAigcMeta } from '../src/export/aigc-export';
import { getLatestResult } from '../src/stores/latest-result.store';

export default function ResultPage() {
  const [message, setMessage] = useState('Choose next action');
  const [latest, setLatest] = useState(() => getLatestResult());
  const router = useRouter();

  useEffect(() => {
    setLatest(getLatestResult());
  }, []);

  async function onSave() {
    const exported = await exportWithAigcMeta(latest?.imageUri ?? 'file://latest-result.png');
    setMessage(`Saved with watermark: ${exported.watermark}`);
  }

  function onContinueEdit() {
    setMessage('Continue editing current result');
    router.push('/editor');
  }

  function onRetry() {
    setMessage('Retry from chat');
    router.push('/chat');
  }

  return (
    <SafeAreaView style={{ flex: 1, padding: 16, backgroundColor: '#F5F7FB' }}>
      <Text style={{ fontSize: 24, fontWeight: '700', marginBottom: 12 }}>
        A-Result
      </Text>
      <ScrollView contentContainerStyle={{ gap: 10 }}>
        {latest?.imageUri ? (
          <View
            style={{
              borderWidth: 1,
              borderColor: '#E2E8F0',
              borderRadius: 10,
              padding: 12,
              backgroundColor: '#FFFFFF',
            }}
          >
            <Text style={{ fontWeight: '700', marginBottom: 8 }}>Latest Preview</Text>
            <Image
              testID="result-preview-image"
              source={{ uri: latest.imageUri }}
              resizeMode="cover"
              style={{
                width: '100%',
                height: 280,
                borderRadius: 8,
                backgroundColor: '#E5E7EB',
              }}
            />
            {latest.prompt ? (
              <Text numberOfLines={4} style={{ marginTop: 8, color: '#334155' }}>
                Prompt: {latest.prompt}
              </Text>
            ) : null}
          </View>
        ) : (
          <Text style={{ color: '#475569' }}>
            No generated image yet. Go to chat and generate one first.
          </Text>
        )}

        <Button title="Save" onPress={onSave} />
        <Button title="Continue Edit" onPress={onContinueEdit} />
        <Button title="Retry" onPress={onRetry} />
        <Text>{message}</Text>
      </ScrollView>
    </SafeAreaView>
  );
}
