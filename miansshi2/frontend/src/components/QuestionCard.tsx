// QuestionCard.tsx - 题目卡片组件
import {
  useJobCategory,
  useCurrentQuestion,
  useIsGeneratingQuestion,
  useSetCurrentQuestion,
  useSetAnswerText,
  useSetGeneratingQuestion,
} from '../store'
import { generateQuestion } from '../api'
import { useState, useCallback, memo } from 'react'
import type { QuestionType } from '../types'

const QUESTION_TYPES: QuestionType[] = [
  '综合分析',
  '计划组织',
  '应急应变',
  '人际关系',
  '情景模拟',
]

export const QuestionCard = memo(function QuestionCard() {
  const jobCategory = useJobCategory()
  const currentQuestion = useCurrentQuestion()
  const isGeneratingQuestion = useIsGeneratingQuestion()
  const setCurrentQuestion = useSetCurrentQuestion()
  const setAnswerText = useSetAnswerText()
  const setGeneratingQuestion = useSetGeneratingQuestion()

  const [selectedType, setSelectedType] = useState<QuestionType>('综合分析')

  const handleGenerateQuestion = useCallback(async () => {
    if (!jobCategory) return

    setGeneratingQuestion(true)
    setAnswerText('')

    try {
      const question = await generateQuestion(jobCategory, selectedType)
      setCurrentQuestion(question)
    } catch (error) {
      console.error('生成题目失败:', error)
      alert('生成题目失败，请稍后重试')
    } finally {
      setGeneratingQuestion(false)
    }
  }, [jobCategory, selectedType, setCurrentQuestion, setAnswerText, setGeneratingQuestion])

  const handleSelectType = useCallback((type: QuestionType) => {
    setSelectedType(type)
  }, [])

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800">面试题目</h3>
        {currentQuestion && (
          <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
            {currentQuestion.question_type}
          </span>
        )}
      </div>

      <div className="flex gap-2 flex-wrap">
        {QUESTION_TYPES.map((type) => (
          <button
            key={type}
            onClick={() => handleSelectType(type)}
            className={`px-3 py-1.5 text-sm rounded-full border transition-all ${
              selectedType === type
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-white text-gray-600 border-gray-300 hover:border-blue-300'
            }`}
          >
            {type}
          </button>
        ))}
      </div>

      <button
        onClick={handleGenerateQuestion}
        disabled={!jobCategory || isGeneratingQuestion}
        className={`w-full py-2.5 rounded-lg font-medium transition-all ${
          !jobCategory || isGeneratingQuestion
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600'
        }`}
      >
        {isGeneratingQuestion ? '生成中...' : '生成题目'}
      </button>

      {currentQuestion && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p className="text-gray-800 leading-relaxed">{currentQuestion.question_text}</p>
          <div className="mt-3 text-sm text-gray-500 flex gap-4">
            <span>思考时间: {currentQuestion.time_limit / 60} 分钟</span>
            <span>作答时间: {currentQuestion.answer_time / 60} 分钟</span>
          </div>
        </div>
      )}
    </div>
  )
})
