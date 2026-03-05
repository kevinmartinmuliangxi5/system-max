import { Link } from 'expo-router';
import { useState } from 'react';
import {
  ActivityIndicator,
  Button,
  SafeAreaView,
  Text,
  TextInput,
  View,
} from 'react-native';

import { mapErrorMessage } from '../src/errors/map-error';
import { inpaintImage } from '../src/flows/inpaint-image';
import { getApiKey } from '../src/security/secure-key';

function readStatusCode(error: unknown): number | undefined {
  const status = (error as { response?: { status?: number } })?.response?.status;
  return typeof status === 'number' ? status : undefined;
}

function readErrorCode(error: unknown): string | undefined {
  const code = (error as { code?: string })?.code;
  return typeof code === 'string' ? code : undefined;
}

export default function EditorPage() {
  const [instruction, setInstruction] = useState('');
  const [imageUri, setImageUri] = useState('file://selected-origin.png');
  const [maskUri, setMaskUri] = useState('file://selected-mask.png');
  const [submitting, setSubmitting] = useState(false);
  const [updatedImageUri, setUpdatedImageUri] = useState<string | undefined>();
  const [errorMessage, setErrorMessage] = useState<string | undefined>();

  async function onApplyInpaint() {
    if (!instruction.trim() || !imageUri.trim() || !maskUri.trim() || submitting) {
      return;
    }

    setSubmitting(true);
    setErrorMessage(undefined);

    try {
      const key = (await getApiKey())?.trim();
      if (!key) {
        setErrorMessage('Missing API key. Save your key first.');
        return;
      }

      const result = await inpaintImage({
        key,
        prompt: instruction.trim(),
        imageUri: imageUri.trim(),
        maskUri: maskUri.trim(),
        conversationId: 'conv_primary',
      });
      setUpdatedImageUri(result.updatedImageUri);
    } catch (error) {
      setErrorMessage(
        mapErrorMessage({
          status: readStatusCode(error),
          code: readErrorCode(error),
        })
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, padding: 16, backgroundColor: '#F2F6FC' }}>
      <Text style={{ fontSize: 24, fontWeight: '700', marginBottom: 12 }}>
        A-Editor
      </Text>
      <View style={{ gap: 12 }}>
        <TextInput
          testID="source-image-uri-input"
          nativeID="source-image-uri-input"
          accessibilityLabel="source-image-uri-input"
          value={imageUri}
          onChangeText={setImageUri}
          placeholder="Source image URI (file://...)"
          autoCapitalize="none"
          style={{
            borderWidth: 1,
            borderColor: '#CBD5E1',
            borderRadius: 8,
            paddingHorizontal: 12,
            paddingVertical: 10,
            backgroundColor: '#FFFFFF',
          }}
        />
        <TextInput
          testID="mask-uri-input"
          nativeID="mask-uri-input"
          accessibilityLabel="mask-uri-input"
          value={maskUri}
          onChangeText={setMaskUri}
          placeholder="Mask URI (file://...)"
          autoCapitalize="none"
          style={{
            borderWidth: 1,
            borderColor: '#CBD5E1',
            borderRadius: 8,
            paddingHorizontal: 12,
            paddingVertical: 10,
            backgroundColor: '#FFFFFF',
          }}
        />
        <TextInput
          testID="inpaint-instruction-input"
          nativeID="inpaint-instruction-input"
          accessibilityLabel="inpaint-instruction-input"
          value={instruction}
          onChangeText={setInstruction}
          placeholder="Describe inpaint instruction"
          style={{
            borderWidth: 1,
            borderColor: '#CBD5E1',
            borderRadius: 8,
            paddingHorizontal: 12,
            paddingVertical: 10,
            backgroundColor: '#FFFFFF',
          }}
        />
        <Button
          testID="apply-inpaint-btn"
          title={submitting ? 'Applying...' : 'Apply'}
          onPress={onApplyInpaint}
          disabled={submitting || !instruction.trim()}
        />
        {submitting ? (
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
            <ActivityIndicator />
            <Text>Inpainting...</Text>
          </View>
        ) : null}
        {updatedImageUri ? (
          <Text testID="updated-uri-text">Updated URI: {updatedImageUri}</Text>
        ) : null}
        {errorMessage ? (
          <Text style={{ color: '#B91C1C' }}>{errorMessage}</Text>
        ) : null}
      </View>
      <View style={{ marginTop: 16, gap: 8 }}>
        <Link href="/chat">Back to Chat</Link>
        <Link href="/result">Go to Result</Link>
      </View>
    </SafeAreaView>
  );
}
