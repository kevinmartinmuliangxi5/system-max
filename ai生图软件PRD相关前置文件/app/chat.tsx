import { Link } from 'expo-router';
import {
  ActivityIndicator,
  Image,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import { useChatStore } from '../src/stores/chat.store';

export default function ChatPage() {
  const {
    state,
    canSubmit,
    setPrompt,
    setApiKeyInput,
    persistApiKey,
    submitPrompt,
  } = useChatStore();
  const saveDisabled = state.apiKeyInput.trim().length === 0;
  const sendDisabled = !canSubmit;

  return (
    <SafeAreaView style={styles.page}>
      <View style={styles.statusBar}>
        <Text style={styles.statusTime}>9:41</Text>
        <Text style={styles.statusSignal}>5G ||| 82%</Text>
      </View>

      <ScrollView style={styles.contentScroll} contentContainerStyle={styles.contentWrapper}>
        <View style={styles.headerRow}>
          <View style={styles.headerTitleWrap}>
            <Text style={styles.caption}>A-ENTERPRISE</Text>
            <Text style={styles.title}>AI 生成控制台</Text>
          </View>
          <Pressable style={styles.newButton}>
            <Text style={styles.newButtonText}>新建</Text>
          </Pressable>
        </View>

        <View style={styles.kpiRow}>
          <View style={styles.kpiCard} testID="chat-latency-kpi">
            <Text style={styles.kpiLabel}>P50</Text>
            <Text style={styles.kpiValue}>6.2s</Text>
          </View>
          <View style={styles.kpiCard} testID="chat-cost-kpi">
            <Text style={styles.kpiLabel}>Cost</Text>
            <Text style={styles.kpiValue}>$0.017</Text>
          </View>
          <View style={styles.kpiCard} testID="chat-retry-kpi">
            <Text style={styles.kpiLabel}>Retry</Text>
            <Text style={styles.kpiValue}>3.4%</Text>
          </View>
        </View>

        <View style={styles.mainCard}>
          <View style={styles.promptCard}>
            <Text style={styles.promptLabel}>Prompt</Text>
            <Text style={styles.promptBody} numberOfLines={2}>
              {state.enhancedPrompt || state.prompt || '输入下一条指令...'}
            </Text>
          </View>

          <View style={styles.byokCard}>
            <Text style={styles.byokTitle}>BYOK Secure</Text>
            <Text style={styles.byokBody}>
              {state.hasApiKey
                ? 'Local keychain storage enabled, logs are masked'
                : 'No key detected. Save API key to local keychain first'}
            </Text>
          </View>

          <View style={styles.inputRow}>
            <TextInput
              testID="api-key-input"
              nativeID="api-key-input"
              accessibilityLabel="api-key-input"
              value={state.apiKeyInput}
              onChangeText={setApiKeyInput}
              placeholder="输入 SiliconFlow API Key"
              autoCapitalize="none"
              autoCorrect={false}
              style={styles.input}
            />
            <Pressable
              testID="save-api-key-btn"
              onPress={persistApiKey}
              disabled={saveDisabled}
              style={({ pressed }) => [
                styles.primaryAction,
                saveDisabled && styles.actionDisabled,
                pressed && !saveDisabled && styles.actionPressed,
              ]}
            >
              <Text style={styles.primaryActionText}>保存</Text>
            </Pressable>
          </View>

          <View style={styles.inputRow}>
            <TextInput
              testID="prompt-input"
              nativeID="prompt-input"
              accessibilityLabel="prompt-input"
              value={state.prompt}
              onChangeText={setPrompt}
              placeholder="输入下一条指令..."
              style={styles.input}
            />
            <Pressable
              testID="send-btn"
              onPress={submitPrompt}
              disabled={sendDisabled}
              style={({ pressed }) => [
                styles.primaryAction,
                sendDisabled && styles.actionDisabled,
                pressed && !sendDisabled && styles.actionPressed,
              ]}
            >
              <Text style={styles.primaryActionText}>
                {state.status === 'submitting' ? '生成中' : '发送'}
              </Text>
            </Pressable>
          </View>

          {state.status === 'submitting' ? (
            <View style={styles.loadingRow}>
              <ActivityIndicator size="small" color="#1D4ED8" />
              <Text style={styles.loadingText}>Generating first image...</Text>
            </View>
          ) : null}

          {state.imageUri ? (
            <View style={styles.resultCard}>
              <Text style={styles.resultTitle}>Result Card</Text>
              <Image
                testID="chat-preview-image"
                source={{ uri: state.imageUri }}
                resizeMode="cover"
                style={styles.previewImage}
              />
              <Text numberOfLines={1} style={styles.resultUri}>
                URI: {state.imageUri}
              </Text>
            </View>
          ) : null}

          {state.errorMessage ? (
            <Text style={styles.errorText}>{state.errorMessage}</Text>
          ) : null}
        </View>
      </ScrollView>

      <View style={styles.bottomTabContainer}>
        <View style={styles.bottomPill} testID="chat-bottom-pill">
          <View style={styles.tabActive}>
            <Text style={styles.tabActiveText}>CHAT</Text>
          </View>
          <Link href="/editor" asChild>
            <Pressable style={styles.tabIdle}>
              <Text style={styles.tabIdleText}>EDITOR</Text>
            </Pressable>
          </Link>
          <Link href="/result" asChild>
            <Pressable style={styles.tabIdle}>
              <Text style={styles.tabIdleText}>RESULT</Text>
            </Pressable>
          </Link>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: {
    flex: 1,
    backgroundColor: '#F5F7FB',
  },
  statusBar: {
    height: 62,
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  statusTime: {
    fontFamily: 'Inter',
    fontSize: 14,
    fontWeight: '600',
    color: '#0F172A',
  },
  statusSignal: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '500',
    color: '#334155',
  },
  contentScroll: {
    flex: 1,
  },
  contentWrapper: {
    padding: 16,
    gap: 12,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitleWrap: {
    gap: 4,
  },
  caption: {
    fontFamily: 'Inter',
    fontSize: 11,
    fontWeight: '700',
    color: '#64748B',
    letterSpacing: 0.6,
  },
  title: {
    fontFamily: 'Inter',
    fontSize: 24,
    fontWeight: '700',
    color: '#0B1B35',
  },
  newButton: {
    backgroundColor: '#1D4ED8',
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 12,
  },
  newButtonText: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  kpiRow: {
    flexDirection: 'row',
    gap: 8,
  },
  kpiCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 10,
    gap: 2,
  },
  kpiLabel: {
    fontFamily: 'Inter',
    fontSize: 10,
    fontWeight: '700',
    color: '#64748B',
  },
  kpiValue: {
    fontFamily: 'Inter',
    fontSize: 14,
    fontWeight: '700',
    color: '#0B1B35',
  },
  mainCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 10,
    gap: 8,
  },
  promptCard: {
    backgroundColor: '#EFF6FF',
    borderRadius: 10,
    padding: 10,
    gap: 4,
  },
  promptLabel: {
    fontFamily: 'Inter',
    fontSize: 10,
    fontWeight: '700',
    color: '#1E3A8A',
  },
  promptBody: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '500',
    color: '#334155',
  },
  byokCard: {
    backgroundColor: '#ECFDF5',
    borderRadius: 10,
    padding: 10,
    gap: 4,
  },
  byokTitle: {
    fontFamily: 'Inter',
    fontSize: 10,
    fontWeight: '700',
    color: '#065F46',
  },
  byokBody: {
    fontFamily: 'Inter',
    fontSize: 11,
    fontWeight: '500',
    color: '#065F46',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#CBD5E1',
    paddingHorizontal: 10,
    paddingVertical: 10,
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '500',
    color: '#334155',
  },
  primaryAction: {
    width: 72,
    backgroundColor: '#1D4ED8',
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
  },
  actionDisabled: {
    opacity: 0.5,
  },
  actionPressed: {
    opacity: 0.85,
  },
  primaryActionText: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  loadingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  loadingText: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '500',
    color: '#334155',
  },
  resultCard: {
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    padding: 10,
    gap: 6,
  },
  resultTitle: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '700',
    color: '#0B1B35',
  },
  previewImage: {
    width: '100%',
    height: 220,
    borderRadius: 8,
    backgroundColor: '#E5E7EB',
  },
  resultUri: {
    fontFamily: 'Inter',
    fontSize: 11,
    fontWeight: '500',
    color: '#334155',
  },
  errorText: {
    fontFamily: 'Inter',
    fontSize: 12,
    fontWeight: '600',
    color: '#B91C1C',
  },
  bottomTabContainer: {
    height: 84,
    padding: 12,
  },
  bottomPill: {
    height: 62,
    borderRadius: 36,
    padding: 4,
    backgroundColor: '#EEF2FF',
    flexDirection: 'row',
    gap: 4,
  },
  tabActive: {
    flex: 1,
    borderRadius: 26,
    backgroundColor: '#1D4ED8',
    alignItems: 'center',
    justifyContent: 'center',
  },
  tabActiveText: {
    fontFamily: 'Inter',
    fontSize: 10,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  tabIdle: {
    flex: 1,
    borderRadius: 26,
    alignItems: 'center',
    justifyContent: 'center',
  },
  tabIdleText: {
    fontFamily: 'Inter',
    fontSize: 10,
    fontWeight: '600',
    color: '#64748B',
  },
});
