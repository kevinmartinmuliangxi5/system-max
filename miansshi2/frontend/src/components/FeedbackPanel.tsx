// FeedbackPanel.tsx - 反馈面板组件
import {
  useCurrentQuestion,
  useJobCategory,
  useSpecificJob,
  useWeights,
  useAnswerText,
  useFeedback,
  useIsSubmittingAnswer,
  useSetFeedback,
  useSetSubmittingAnswer,
} from '../store'
import { submitFeedback } from '../api'
import { useCallback, memo } from 'react'

export const FeedbackPanel = memo(function FeedbackPanel() {
  const currentQuestion = useCurrentQuestion()
  const jobCategory = useJobCategory()
  const specificJob = useSpecificJob()
  const weights = useWeights()
  const answerText = useAnswerText()
  const feedback = useFeedback()
  const isSubmittingAnswer = useIsSubmittingAnswer()
  const setFeedback = useSetFeedback()
  const setSubmittingAnswer = useSetSubmittingAnswer()

  const handleSubmit = useCallback(async () => {
    if (!currentQuestion || !jobCategory || answerText.length < 10) return

    setSubmittingAnswer(true)
    try {
      const result = await submitFeedback(
        currentQuestion,
        jobCategory,
        specificJob || '未指定岗位',
        weights,
        answerText
      )
      setFeedback(result)
    } catch (error) {
      console.error('提交失败:', error)
      setFeedback({ success: false, error: '提交失败，请稍后重试' })
    } finally {
      setSubmittingAnswer(false)
    }
  }, [currentQuestion, jobCategory, answerText, specificJob, weights, setFeedback, setSubmittingAnswer])

  if (!currentQuestion) {
    return (
      <div className="h-full bg-white rounded-xl border border-gray-200 p-6 flex flex-col">
        <h3 className="text-base font-semibold text-gray-900">AI 评分反馈</h3>
        <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
          生成题目后开始练习
        </div>
      </div>
    )
  }

  const canSubmit = answerText.length >= 10 && !isSubmittingAnswer

  return (
    <div className="h-full bg-white rounded-xl border border-gray-200 p-6 flex flex-col">
      {/* 标题 */}
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-base font-semibold text-gray-900">AI 评分反馈</h3>
        {feedback?.success && (
          <span className="px-2 py-1 bg-gray-900 text-white text-xs rounded">
            已完成
          </span>
        )}
      </div>

      {/* 提交按钮 */}
      {!feedback?.success && (
        <button
          onClick={handleSubmit}
          disabled={!canSubmit}
          className={`w-full py-3 rounded-lg font-medium transition-all mb-5 ${
            !canSubmit
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-red-600 text-white hover:bg-red-700'
          }`}
        >
          {isSubmittingAnswer ? 'AI 评分中...' : '提交获取反馈'}
        </button>
      )}

      {/* 等待状态 */}
      {!feedback && !isSubmittingAnswer && (
        <div className="flex-1 flex items-center justify-center text-center text-gray-400 text-sm">
          <div>
            <p>提交答案后</p>
            <p>AI 将给出评分和改进建议</p>
          </div>
        </div>
      )}

      {/* 错误提示 */}
      {feedback && !feedback.success && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 text-sm">
          {feedback.error}
        </div>
      )}

      {/* 反馈结果 */}
      {feedback?.success && (
        <div className="flex-1 overflow-auto space-y-4">
          {/* 综合得分 */}
          <div className="bg-slate-50 rounded-xl p-5 text-center">
            <div className="text-5xl font-bold text-red-600">{feedback.total_score}</div>
            <div className="text-sm text-gray-500 mt-1">综合得分</div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
              <div
                className="bg-red-600 h-2 rounded-full transition-all"
                style={{ width: `${feedback.total_score}%` }}
              />
            </div>
          </div>

          {/* 分项得分 */}
          {feedback.score_breakdown && (
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(feedback.score_breakdown).map(([key, value]) => (
                <div key={key} className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500">{key}</div>
                  <div className="text-lg font-semibold text-gray-800">{value}</div>
                </div>
              ))}
            </div>
          )}

          {/* 评分溯源 */}
          {feedback.traces && feedback.traces.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-800">评分溯源</h4>
              <div className="max-h-40 overflow-auto space-y-2">
                {feedback.traces.map((trace, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border text-sm ${
                      trace.score_change >= 0
                        ? 'bg-green-50 border-green-200'
                        : 'bg-red-50 border-red-200'
                    }`}
                  >
                    <div className="font-medium text-gray-800">"{trace.quote}"</div>
                    <div className="text-gray-600 mt-1">{trace.analysis}</div>
                    <div
                      className={`text-xs font-medium mt-1 ${
                        trace.score_change >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {trace.score_change >= 0 ? '+' : ''}
                      {trace.score_change} 分
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 逻辑诊断 */}
          {feedback.logic_diagnosis && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-yellow-800 mb-2">逻辑诊断</h4>
              <p className="text-yellow-700 text-sm">{feedback.logic_diagnosis}</p>
            </div>
          )}

          {/* 改进建议 */}
          {feedback.improvement_tips && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-blue-800 mb-2">改进建议</h4>
              <p className="text-blue-700 text-sm">{feedback.improvement_tips}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
})
