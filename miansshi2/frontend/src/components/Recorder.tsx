// Recorder.tsx - 录音组件
import { useAnswerText, useCurrentQuestion, useSetAnswerText } from '../store'
import { useRecording } from '../hooks/useRecording'
import { useEffect, useCallback, memo, useState } from 'react'

export const Recorder = memo(function Recorder() {
  const answerText = useAnswerText()
  const currentQuestion = useCurrentQuestion()
  const setAnswerText = useSetAnswerText()
  const [inputMode, setInputMode] = useState<'voice' | 'text'>('voice')

  const { state, transcript, startRecording, stopRecording, resetTranscript, isRecording } =
    useRecording({
      onResult: (text) => {
        setAnswerText(text)
      },
      onError: (error) => {
        alert(`录音错误: ${error}`)
      },
    })

  // 重置录音文本
  useEffect(() => {
    resetTranscript()
  }, [currentQuestion, resetTranscript])

  const handleToggleRecording = useCallback(() => {
    if (isRecording) {
      stopRecording()
    } else {
      startRecording()
    }
  }, [isRecording, startRecording, stopRecording])

  const handleAnswerChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setAnswerText(e.target.value)
  }, [setAnswerText])

  const handleClear = useCallback(() => {
    setAnswerText('')
    resetTranscript()
  }, [setAnswerText, resetTranscript])

  if (!currentQuestion) return null

  return (
    <div className="flex flex-col items-center justify-center h-full w-full">
      {inputMode === 'voice' ? (
        <>
          {/* 大录音按钮 */}
          <button
            onClick={handleToggleRecording}
            className={`w-24 h-24 rounded-full flex items-center justify-center transition-all ${
              isRecording
                ? 'bg-red-600 animate-pulse shadow-lg shadow-red-200'
                : 'bg-red-600 hover:bg-red-700 shadow-lg'
            }`}
          >
            {isRecording ? (
              <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            ) : (
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>

          <p className="mt-5 text-sm text-gray-500">
            {isRecording ? '点击停止录音' : '点击开始录音'}
          </p>
          <p className="mt-1 text-xs text-gray-400">停顿30秒自动结束</p>

          {/* 错误提示 */}
          {state.status === 'error' && (
            <div className="mt-4 text-red-500 text-sm">{state.error}</div>
          )}

          {/* 识别结果预览 */}
          {transcript && (
            <div className="mt-4 text-sm text-gray-600 max-w-md text-center">
              识别中: {transcript}
            </div>
          )}

          {/* 切换到文字模式 */}
          <button
            onClick={() => setInputMode('text')}
            className="mt-6 text-xs text-gray-400 hover:text-gray-600"
          >
            或使用文字输入 →
          </button>
        </>
      ) : (
        <>
          {/* 文字输入模式 */}
          <div className="w-full max-w-lg">
            <textarea
              value={answerText}
              onChange={handleAnswerChange}
              placeholder="在此输入答案..."
              rows={6}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 resize-none text-sm"
            />
            <div className="flex justify-between items-center mt-2">
              <span className="text-xs text-gray-400">
                {answerText.length} / 5000 字符
              </span>
              <button
                onClick={() => setInputMode('voice')}
                className="text-xs text-red-600 hover:text-red-700"
              >
                ← 切换到语音模式
              </button>
            </div>
          </div>
        </>
      )}

      {/* 底部操作按钮 - 有内容时显示 */}
      {answerText && (
        <div className="flex gap-3 mt-6 w-full max-w-lg">
          <button
            onClick={handleClear}
            className="flex-1 flex items-center justify-center gap-2 py-3 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            清空
          </button>
          <button
            onClick={() => {
              // 触发提交 - FeedbackPanel 会监听 answerText 变化
            }}
            className="flex-1 flex items-center justify-center gap-2 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            提交答案
          </button>
        </div>
      )}
    </div>
  )
})
