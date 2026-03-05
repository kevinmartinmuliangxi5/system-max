// store.ts - Zustand 状态管理
import { create } from 'zustand'
import type { JobCategory, Question, Weights, Feedback, RecordingState, ExamState } from './types'

interface AppState {
  // 岗位配置
  jobCategory: JobCategory | null
  sliderValue: number
  weights: Weights
  specificJob: string

  // 当前题目
  currentQuestion: Question | null
  answerText: string

  // AI 反馈
  feedback: Feedback | null
  isGeneratingQuestion: boolean
  isSubmittingAnswer: boolean

  // 录音状态
  recordingState: RecordingState

  // 考试模式
  examState: ExamState | null

  // Actions
  setJobCategory: (category: JobCategory) => void
  setSliderValue: (value: number) => void
  setWeights: (weights: Weights) => void
  setSpecificJob: (job: string) => void
  setCurrentQuestion: (question: Question | null) => void
  setAnswerText: (text: string) => void
  setFeedback: (feedback: Feedback | null) => void
  setGeneratingQuestion: (isGenerating: boolean) => void
  setSubmittingAnswer: (isSubmitting: boolean) => void
  setRecordingState: (state: RecordingState) => void
  setExamState: (state: ExamState | null) => void
  reset: () => void
}

const initialState = {
  jobCategory: null,
  sliderValue: 0,
  weights: { logic: 0.25, principle: 0.25, empathy: 0.25, expression: 0.25 },
  specificJob: '',
  currentQuestion: null,
  answerText: '',
  feedback: null,
  isGeneratingQuestion: false,
  isSubmittingAnswer: false,
  recordingState: { status: 'idle' as const },
  examState: null,
}

export const useStore = create<AppState>((set) => ({
  ...initialState,

  setJobCategory: (category) => set({ jobCategory: category }),
  setSliderValue: (value) => set({ sliderValue: value }),
  setWeights: (weights) => set({ weights }),
  setSpecificJob: (job) => set({ specificJob: job }),
  setCurrentQuestion: (question) => set({ currentQuestion: question, feedback: null }),
  setAnswerText: (text) => set({ answerText: text }),
  setFeedback: (feedback) => set({ feedback }),
  setGeneratingQuestion: (isGenerating) => set({ isGeneratingQuestion: isGenerating }),
  setSubmittingAnswer: (isSubmitting) => set({ isSubmittingAnswer: isSubmitting }),
  setRecordingState: (state) => set({ recordingState: state }),
  setExamState: (state) => set({ examState: state }),

  reset: () => set(initialState),
}))

// ============ 选择器 Hooks (性能优化) ============

// 岗位相关选择器
export const useJobCategory = () => useStore((state) => state.jobCategory)
export const useSliderValue = () => useStore((state) => state.sliderValue)
export const useWeights = () => useStore((state) => state.weights)
export const useSpecificJob = () => useStore((state) => state.specificJob)

// 题目相关选择器
export const useCurrentQuestion = () => useStore((state) => state.currentQuestion)
export const useAnswerText = () => useStore((state) => state.answerText)

// 反馈相关选择器
export const useFeedback = () => useStore((state) => state.feedback)
export const useIsGeneratingQuestion = () => useStore((state) => state.isGeneratingQuestion)
export const useIsSubmittingAnswer = () => useStore((state) => state.isSubmittingAnswer)

// 考试模式选择器
export const useExamState = () => useStore((state) => state.examState)

// ============ Actions (稳定引用) ============
// 直接从 store 获取 actions，避免每次渲染创建新对象

// 岗位 Actions
export const useSetJobCategory = () => useStore((state) => state.setJobCategory)
export const useSetSliderValue = () => useStore((state) => state.setSliderValue)
export const useSetWeights = () => useStore((state) => state.setWeights)
export const useSetSpecificJob = () => useStore((state) => state.setSpecificJob)

// 题目 Actions
export const useSetCurrentQuestion = () => useStore((state) => state.setCurrentQuestion)
export const useSetAnswerText = () => useStore((state) => state.setAnswerText)

// 反馈 Actions
export const useSetFeedback = () => useStore((state) => state.setFeedback)
export const useSetGeneratingQuestion = () => useStore((state) => state.setGeneratingQuestion)
export const useSetSubmittingAnswer = () => useStore((state) => state.setSubmittingAnswer)

// 录音 Actions
export const useSetRecordingState = () => useStore((state) => state.setRecordingState)

// 考试 Actions
export const useSetExamState = () => useStore((state) => state.setExamState)

// Reset
export const useReset = () => useStore((state) => state.reset)
