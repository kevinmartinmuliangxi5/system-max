// api.ts - API 调用封装
import axios from 'axios'
import type { JobInfo, Weights, Question, Feedback, JobCategory, QuestionType } from './types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ============ 运行时类型验证 ============

function validateWeights(data: unknown): Weights {
  if (typeof data !== 'object' || data === null) {
    throw new Error('权重数据格式错误')
  }
  const obj = data as Record<string, unknown>
  const weights: Weights = {
    logic: Number(obj.logic) || 0,
    principle: Number(obj.principle) || 0,
    empathy: Number(obj.empathy) || 0,
    expression: Number(obj.expression) || 0,
  }
  return weights
}

function validateQuestion(data: unknown): Question {
  if (typeof data !== 'object' || data === null) {
    throw new Error('题目数据格式错误')
  }
  const obj = data as Record<string, unknown>
  if (!obj.question_id || !obj.question_text || !obj.question_type) {
    throw new Error('题目数据缺少必要字段')
  }
  return {
    question_id: String(obj.question_id),
    question_text: String(obj.question_text),
    question_type: obj.question_type as QuestionType,
    time_limit: Number(obj.time_limit) || 240,
    answer_time: Number(obj.answer_time) || 180,
  }
}

function validateFeedback(data: unknown): Feedback {
  if (typeof data !== 'object' || data === null) {
    throw new Error('反馈数据格式错误')
  }
  const obj = data as Record<string, unknown>
  return {
    success: Boolean(obj.success),
    total_score: obj.total_score !== undefined ? Number(obj.total_score) : undefined,
    score_breakdown:
      obj.score_breakdown !== undefined
        ? (obj.score_breakdown as Record<string, number>)
        : undefined,
    traces: Array.isArray(obj.traces) ? obj.traces : undefined,
    logic_diagnosis: obj.logic_diagnosis !== undefined ? String(obj.logic_diagnosis) : undefined,
    improvement_tips:
      obj.improvement_tips !== undefined ? String(obj.improvement_tips) : undefined,
    error: obj.error !== undefined ? String(obj.error) : undefined,
  }
}

// ============ REST API ============

export async function getJobs(): Promise<JobInfo[]> {
  const response = await api.get('/jobs')
  if (!Array.isArray(response.data)) {
    throw new Error('岗位数据格式错误')
  }
  return response.data
}

export async function getQuestionTypes(): Promise<string[]> {
  const response = await api.get('/question-types')
  if (!Array.isArray(response.data)) {
    throw new Error('题型数据格式错误')
  }
  return response.data
}

export async function computeWeights(
  category: JobCategory,
  sliderValue: number
): Promise<Weights> {
  const response = await api.post('/weights', {
    category,
    slider_value: sliderValue,
  })
  return validateWeights(response.data)
}

export async function generateQuestion(
  category: JobCategory,
  questionType: QuestionType,
  difficulty: string = 'medium'
): Promise<Question> {
  const response = await api.post('/question', {
    category,
    question_type: questionType,
    difficulty,
  })
  return validateQuestion(response.data)
}

export async function submitFeedback(
  question: Question,
  category: JobCategory,
  specificJob: string,
  weights: Weights,
  answerText: string
): Promise<Feedback> {
  const response = await api.post('/feedback', {
    question_id: question.question_id,
    question_text: question.question_text,
    question_type: question.question_type,
    category,
    specific_job: specificJob,
    weights,
    answer_text: answerText,
  })
  return validateFeedback(response.data)
}

// ============ WebSocket 语音识别 ============

export class SpeechWebSocket {
  private ws: WebSocket | null = null
  private onResult: (text: string, isFinal: boolean) => void
  private onError: (error: string) => void

  constructor(
    onResult: (text: string, isFinal: boolean) => void,
    onError: (error: string) => void
  ) {
    this.onResult = onResult
    this.onError = onError
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      // 构建 WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const wsUrl = `${protocol}//${host}/api/ws/speech`

      console.log('[WebSocket] 正在连接:', wsUrl)
      console.log('[WebSocket] 当前页面 Origin:', window.location.origin)

      try {
        this.ws = new WebSocket(wsUrl)

        // 设置连接超时
        const timeout = setTimeout(() => {
          if (this.ws && this.ws.readyState !== WebSocket.OPEN) {
            console.error('[WebSocket] 连接超时')
            this.ws.close()
            this.onError('WebSocket 连接超时，请检查后端服务是否运行')
            reject(new Error('Connection timeout'))
          }
        }, 10000)

        this.ws.onopen = () => {
          clearTimeout(timeout)
          console.log('[WebSocket] 连接成功')
          resolve()
        }

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            console.log('[WebSocket] 收到消息:', data)
            this.onResult(data.text, data.is_final)

            if (data.error) {
              this.onError(data.error)
            }

            // 收到最终结果后，自动关闭连接
            if (data.is_final) {
              console.log('[WebSocket] 收到最终结果，关闭连接')
              setTimeout(() => {
                if (this.ws) {
                  this.ws.close()
                  this.ws = null
                }
              }, 100)
            }
          } catch (e) {
            console.error('[WebSocket] 消息解析错误:', e)
          }
        }

        this.ws.onerror = (event) => {
          clearTimeout(timeout)
          console.error('[WebSocket] 连接错误:', event)
          this.onError('WebSocket 连接失败，请确保后端服务正在运行 (port 8000)')
          reject(new Error('WebSocket error'))
        }

        this.ws.onclose = (event) => {
          clearTimeout(timeout)
          console.log('[WebSocket] 连接关闭:', event.code, event.reason)
          if (event.code === 4003) {
            this.onError('WebSocket 认证失败，请刷新页面重试')
          }
          this.ws = null
        }
      } catch (error) {
        console.error('[WebSocket] 创建连接失败:', error)
        this.onError('无法创建 WebSocket 连接')
        reject(error)
      }
    })
  }

  start(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'start' }))
    }
  }

  sendAudio(audioData: ArrayBuffer): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const base64 = arrayBufferToBase64(audioData)
      this.ws.send(JSON.stringify({ type: 'audio', audio_data: base64 }))
    }
  }

  stop(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: 'stop' }))
    }
  }

  close(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

// Helper: ArrayBuffer to Base64 (优化 O(n) 性能)
function arrayBufferToBase64(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer)
  // 使用数组 + join 避免 O(n²) 的字符串拼接
  const binaryChunks: string[] = new Array(bytes.byteLength)
  for (let i = 0; i < bytes.byteLength; i++) {
    binaryChunks[i] = String.fromCharCode(bytes[i])
  }
  return btoa(binaryChunks.join(''))
}
