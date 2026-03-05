// Exam.tsx - 模拟考试页面
import { useState, useCallback } from 'react'
import { useJobCategory, useSpecificJob, useWeights, useExamState, useSetExamState } from '../store'
import { generateQuestion, submitFeedback } from '../api'
import { useCountdown } from '../hooks/useTimer'
import type { QuestionType, ExamQuestion, Feedback } from '../types'

const EXAM_QUESTIONS: QuestionType[] = ['综合分析', '应急应变', '人际关系']
const THINK_TIME = 240 // 4 分钟思考
const ANSWER_TIME = 180 // 3 分钟作答

export function Exam() {
  const jobCategory = useJobCategory()
  const specificJob = useSpecificJob()
  const weights = useWeights()
  const examState = useExamState()
  const setExamState = useSetExamState()
  const [isLoading, setIsLoading] = useState(false)
  const [currentAnswer, setCurrentAnswer] = useState('')

  const { formatted, startCountdown, progress } = useCountdown(
    examState?.phase === 'thinking' ? THINK_TIME : ANSWER_TIME,
    () => {
      if (examState?.phase === 'thinking') {
        setExamState({ ...examState, phase: 'answering', startTime: Date.now() })
      } else if (examState?.phase === 'answering') {
        handleNextQuestion()
      }
    }
  )

  // 开始考试
  const startExam = async () => {
    if (!jobCategory) {
      alert('请先在训练模式选择岗位类型')
      return
    }

    setIsLoading(true)
    try {
      const questions: ExamQuestion[] = await Promise.all(
        EXAM_QUESTIONS.map(async (type) => {
          const q = await generateQuestion(jobCategory, type, 'medium')
          return { ...q, answer_text: '' }
        })
      )

      setExamState({
        questions,
        currentIndex: 0,
        phase: 'preparing',
        startTime: null,
      })
    } catch (error) {
      console.error('生成题目失败:', error)
      alert('生成题目失败，请稍后重试')
    } finally {
      setIsLoading(false)
    }
  }

  // 开始答题
  const handleStartAnswer = () => {
    if (!examState) return
    setExamState({ ...examState, phase: 'thinking', startTime: Date.now() })
    startCountdown(THINK_TIME)
  }

  // 开始作答（思考结束）
  const handleStartSpeaking = () => {
    if (!examState) return
    setExamState({ ...examState, phase: 'answering' })
    startCountdown(ANSWER_TIME)
  }

  // 下一题
  const handleNextQuestion = useCallback(async () => {
    if (!examState) return

    const { questions, currentIndex } = examState
    const currentQuestion = questions[currentIndex]
    const answerText = currentAnswer

    // 保存答案
    const updatedQuestions = [...questions]
    updatedQuestions[currentIndex] = { ...currentQuestion, answer_text: answerText }

    // 判断是否完成
    if (currentIndex >= questions.length - 1) {
      setIsLoading(true)
      try {
        const feedbacks: Feedback[] = await Promise.all(
          updatedQuestions.map((q) =>
            submitFeedback(q, jobCategory!, specificJob || '未指定', weights, q.answer_text)
          )
        )

        const finalQuestions = updatedQuestions.map((q, i) => ({
          ...q,
          feedback: feedbacks[i],
        }))

        setExamState({
          ...examState,
          questions: finalQuestions,
          phase: 'completed',
        })
      } catch (error) {
        console.error('获取反馈失败:', error)
      } finally {
        setIsLoading(false)
      }
    } else {
      setCurrentAnswer('')
      setExamState({
        ...examState,
        questions: updatedQuestions,
        currentIndex: currentIndex + 1,
        phase: 'preparing',
        startTime: null,
      })
    }
  }, [examState, currentAnswer, jobCategory, specificJob, weights])

  // 考试未开始
  if (!examState) {
    return (
      <div className="min-h-screen flex items-center justify-center p-10">
        <div className="bg-white rounded-xl border border-gray-200 p-10 max-w-md w-full text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">模拟考试模式</h1>
          <div className="text-gray-600 space-y-2 mb-8">
            <p>共 3 道题目</p>
            <p>每题 {THINK_TIME / 60} 分钟思考 + {ANSWER_TIME / 60} 分钟作答</p>
            <p>全部作答完成后统一评分</p>
          </div>
          <button
            onClick={startExam}
            disabled={!jobCategory || isLoading}
            className={`w-full py-3 rounded-lg font-medium ${
              !jobCategory || isLoading
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-red-600 text-white hover:bg-red-700'
            }`}
          >
            {isLoading ? '准备中...' : '开始考试'}
          </button>
          {!jobCategory && (
            <p className="text-sm text-red-500 mt-4">请先在训练模式选择岗位类型</p>
          )}
        </div>
      </div>
    )
  }

  // 考试完成
  if (examState.phase === 'completed') {
    return (
      <div className="min-h-screen p-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">考试结果</h1>
          <div className="space-y-4">
            {examState.questions.map((q, i) => (
              <div key={i} className="bg-white rounded-xl border border-gray-200 p-6">
                <div className="flex justify-between items-center mb-4">
                  <span className="px-3 py-1 bg-red-50 text-red-600 text-xs font-medium rounded-md">
                    {q.question_type}
                  </span>
                  {q.feedback?.success && (
                    <span className="text-2xl font-bold text-red-600">{q.feedback.total_score}</span>
                  )}
                </div>
                <p className="text-gray-800 mb-4">{q.question_text}</p>
                {q.feedback?.improvement_tips && (
                  <div className="bg-blue-50 rounded-lg p-4 text-sm text-blue-700">
                    {q.feedback.improvement_tips}
                  </div>
                )}
              </div>
            ))}
          </div>
          <button
            onClick={() => setExamState(null)}
            className="w-full mt-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            返回
          </button>
        </div>
      </div>
    )
  }

  // 当前题目
  const currentQ = examState.questions[examState.currentIndex]

  return (
    <div className="min-h-screen p-10">
      <div className="max-w-4xl mx-auto">
        {/* 进度条 */}
        <div className="flex gap-2 mb-6">
          {examState.questions.map((_, i) => (
            <div
              key={i}
              className={`h-2 flex-1 rounded-full ${
                i < examState.currentIndex
                  ? 'bg-green-500'
                  : i === examState.currentIndex
                  ? 'bg-red-600'
                  : 'bg-gray-200'
              }`}
            />
          ))}
        </div>

        {/* 题目卡片 */}
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <div className="flex justify-between items-center mb-4">
            <span className="text-lg font-semibold">第 {examState.currentIndex + 1} 题</span>
            <span className="px-3 py-1 bg-red-50 text-red-600 text-xs font-medium rounded-md">
              {currentQ.question_type}
            </span>
          </div>

          <p className="text-gray-800 text-lg leading-relaxed mb-8">{currentQ.question_text}</p>

          {/* 计时器 */}
          {(examState.phase === 'thinking' || examState.phase === 'answering') && (
            <div className="text-center py-8">
              <div className="text-5xl font-bold text-red-600 mb-4">{formatted}</div>
              <div className="w-full bg-gray-200 rounded-full h-3 max-w-md mx-auto">
                <div
                  className="bg-red-600 h-3 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <div className="text-sm text-gray-500 mt-3">
                {examState.phase === 'thinking' ? '思考时间' : '作答时间'}
              </div>
            </div>
          )}

          {/* 准备阶段 */}
          {examState.phase === 'preparing' && (
            <button
              onClick={handleStartAnswer}
              className="w-full py-4 bg-red-600 text-white rounded-lg hover:bg-red-700 text-lg font-medium"
            >
              开始答题
            </button>
          )}

          {/* 思考阶段 */}
          {examState.phase === 'thinking' && (
            <button
              onClick={handleStartSpeaking}
              className="w-full py-4 bg-green-600 text-white rounded-lg hover:bg-green-700 text-lg font-medium"
            >
              开始作答
            </button>
          )}

          {/* 作答阶段 */}
          {examState.phase === 'answering' && (
            <>
              <textarea
                placeholder="在此输入答案..."
                rows={6}
                className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500 mb-4"
                value={currentAnswer || currentQ.answer_text}
                onChange={(e) => setCurrentAnswer(e.target.value)}
              />
              <button
                onClick={handleNextQuestion}
                className="w-full py-4 bg-red-600 text-white rounded-lg hover:bg-red-700 text-lg font-medium"
              >
                {examState.currentIndex < examState.questions.length - 1 ? '下一题' : '提交答案'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
