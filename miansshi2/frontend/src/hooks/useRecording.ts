// useRecording.ts - 录音 Hook
import { useState, useCallback, useRef, useEffect } from 'react'
import { SpeechWebSocket } from '../api'
import type { RecordingState } from '../types'

interface UseRecordingOptions {
  onResult?: (text: string, isFinal: boolean) => void
  onError?: (error: string) => void
}

// 将音频从任意采样率重采样到 16KHz
function resampleTo16KHz(inputData: Float32Array, inputSampleRate: number): Int16Array {
  const targetSampleRate = 16000
  const ratio = inputSampleRate / targetSampleRate
  const outputLength = Math.floor(inputData.length / ratio)
  const output = new Int16Array(outputLength)

  for (let i = 0; i < outputLength; i++) {
    const srcIndex = i * ratio
    const srcIndexFloor = Math.floor(srcIndex)
    const srcIndexCeil = Math.min(srcIndexFloor + 1, inputData.length - 1)
    const t = srcIndex - srcIndexFloor

    // 线性插值
    const sample = inputData[srcIndexFloor] * (1 - t) + inputData[srcIndexCeil] * t
    // 转换为 16-bit PCM
    const clamped = Math.max(-1, Math.min(1, sample))
    output[i] = clamped < 0 ? clamped * 0x8000 : clamped * 0x7FFF
  }

  return output
}

export function useRecording(options: UseRecordingOptions = {}) {
  const [state, setState] = useState<RecordingState>({ status: 'idle' })
  const [transcript, setTranscript] = useState('')
  const wsRef = useRef<SpeechWebSocket | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const workletRef = useRef<ScriptProcessorNode | null>(null)
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null)

  // 使用 ref 存储回调，避免 useCallback 依赖 options 对象
  const onResultRef = useRef(options.onResult)
  const onErrorRef = useRef(options.onError)

  // 保持 ref 最新
  useEffect(() => {
    onResultRef.current = options.onResult
    onErrorRef.current = options.onError
  }, [options.onResult, options.onError])

  const startRecording = useCallback(async () => {
    try {
      console.log('[录音] 开始请求麦克风权限...')

      // 请求麦克风权限
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          channelCount: 1,
        },
      })
      streamRef.current = stream
      console.log('[录音] 麦克风权限获取成功')

      // 连接 WebSocket
      console.log('[录音] 正在连接 WebSocket...')
      const ws = new SpeechWebSocket(
        (text, isFinal) => {
          console.log('[录音] 收到识别结果:', { text, isFinal })
          setTranscript(text)
          onResultRef.current?.(text, isFinal)
        },
        (error) => {
          console.error('[录音] WebSocket 错误:', error)
          setState({ status: 'error', error })
          onErrorRef.current?.(error)
        }
      )
      await ws.connect()
      ws.start()
      wsRef.current = ws
      console.log('[录音] WebSocket 连接成功')

      // 使用 AudioContext 处理音频
      const audioContext = new AudioContext()
      audioContextRef.current = audioContext
      const actualSampleRate = audioContext.sampleRate
      console.log(`[录音] AudioContext 采样率: ${actualSampleRate}Hz，将重采样到 16000Hz`)

      const source = audioContext.createMediaStreamSource(stream)
      sourceRef.current = source
      const bufferSize = 4096
      const scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1)
      workletRef.current = scriptProcessor

      let chunkCount = 0
      let totalSamples = 0

      scriptProcessor.onaudioprocess = (event) => {
        if (!wsRef.current?.isConnected()) return

        const inputData = event.inputBuffer.getChannelData(0)

        // 重采样到 16KHz 并转换为 16-bit PCM
        const pcmData = resampleTo16KHz(inputData, actualSampleRate)

        // 发送 PCM 数据
        wsRef.current.sendAudio(pcmData.buffer as ArrayBuffer)
        chunkCount++
        totalSamples += inputData.length

        // 每 10 个 chunk 打印一次日志
        if (chunkCount % 10 === 0) {
          const duration = (totalSamples / actualSampleRate).toFixed(1)
          console.log(`[录音] 已发送 ${chunkCount} 个音频块，约 ${duration} 秒音频`)
        }
      }

      source.connect(scriptProcessor)
      scriptProcessor.connect(audioContext.destination)

      setState({ status: 'recording', startTime: Date.now() })
      setTranscript('')
      console.log('[录音] 录音开始')
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '无法访问麦克风'
      console.error('[录音] 启动失败:', error)
      setState({ status: 'error', error: errorMessage })
      onErrorRef.current?.(errorMessage)

      // 清理资源
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
    }
  }, [])

  const stopRecording = useCallback(() => {
    console.log('[录音] 停止录音...')

    // 1. 先断开音频处理（停止发送新数据）
    if (workletRef.current) {
      workletRef.current.disconnect()
      workletRef.current = null
    }
    if (sourceRef.current) {
      sourceRef.current.disconnect()
      sourceRef.current = null
    }
    if (audioContextRef.current) {
      audioContextRef.current.close()
      audioContextRef.current = null
    }

    // 2. 停止麦克风
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }

    // 3. 发送停止信号给后端，等待最终结果
    if (wsRef.current && wsRef.current.isConnected()) {
      console.log('[录音] 发送停止信号给后端，等待最终识别结果...')
      wsRef.current.stop()

      // 等待最终结果或超时（最多等待 30 秒）
      const startTime = Date.now()
      const maxWaitTime = 30000

      const checkFinalResult = () => {
        // 检查是否收到了最终结果（通过 onResult 回调处理）
        // 或者超时
        if (Date.now() - startTime > maxWaitTime) {
          console.log('[录音] 等待最终结果超时，关闭连接')
          if (wsRef.current) {
            wsRef.current.close()
            wsRef.current = null
          }
          setState({ status: 'idle' })
          console.log('[录音] 录音已停止')
        } else if (!wsRef.current || !wsRef.current.isConnected()) {
          // WebSocket 已关闭（可能收到了最终结果后关闭）
          console.log('[录音] 连接已关闭，录音已停止')
          wsRef.current = null
          setState({ status: 'idle' })
        } else {
          // 继续等待
          setTimeout(checkFinalResult, 500)
        }
      }

      // 开始检查
      setTimeout(checkFinalResult, 500)
    } else {
      // 如果 WebSocket 未连接，直接清理
      if (workletRef.current) {
        workletRef.current.disconnect()
        workletRef.current = null
      }
      if (sourceRef.current) {
        sourceRef.current.disconnect()
        sourceRef.current = null
      }
      if (audioContextRef.current) {
        audioContextRef.current.close()
        audioContextRef.current = null
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
      setState({ status: 'idle' })
    }
  }, [])

  const resetTranscript = useCallback(() => {
    setTranscript('')
  }, [])

  // 组件卸载时清理
  useEffect(() => {
    return () => {
      console.log('[录音] 组件卸载，清理资源')
      if (workletRef.current) {
        workletRef.current.disconnect()
      }
      if (audioContextRef.current) {
        audioContextRef.current.close()
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  return {
    state,
    transcript,
    startRecording,
    stopRecording,
    resetTranscript,
    isRecording: state.status === 'recording',
  }
}
