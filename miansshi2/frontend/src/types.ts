// types.ts - TypeScript 类型定义

// ============ 枚举类型 ============

export type JobCategory = '行政执法类' | '窗口服务类' | '综合管理类'

export type QuestionType = '综合分析' | '计划组织' | '应急应变' | '人际关系' | '情景模拟'

// ============ API 响应类型 ============

export interface JobInfo {
  key: JobCategory
  desc: string
  slider_label: string
}

export interface Weights {
  logic: number
  principle: number
  empathy: number
  expression: number
}

export interface Question {
  question_id: string
  question_text: string
  question_type: QuestionType
  time_limit: number
  answer_time: number
}

export interface FeedbackTrace {
  quote: string
  analysis: string
  score_change: number
}

export interface Feedback {
  success: boolean
  total_score?: number
  score_breakdown?: Record<string, number>
  traces?: FeedbackTrace[]
  logic_diagnosis?: string
  improvement_tips?: string
  error?: string
}

// ============ UI 状态类型 ============

// Discriminated Union for Recording State
export type RecordingState =
  | { status: 'idle' }
  | { status: 'recording'; startTime: number }
  | { status: 'processing' }
  | { status: 'error'; error: string }

// API Response Discriminated Union
export type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string }

// ============ 考试模式类型 ============

export interface ExamQuestion extends Question {
  answer_text: string
  feedback?: Feedback
}

export interface ExamState {
  questions: ExamQuestion[]
  currentIndex: number
  phase: 'preparing' | 'thinking' | 'answering' | 'completed'
  startTime: number | null
}
