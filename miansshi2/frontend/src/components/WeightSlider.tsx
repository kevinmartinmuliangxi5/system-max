// WeightSlider.tsx - 权重滑块组件
import { useJobCategory, useSliderValue, useWeights, useSetSliderValue, useSetWeights } from '../store'
import { computeWeights } from '../api'
import { useEffect, useCallback, memo, useRef } from 'react'
import { useDebounce } from '../hooks/useTimer'

const DEBOUNCE_DELAY = 300 // 300ms 防抖延迟

export const WeightSlider = memo(function WeightSlider() {
  const jobCategory = useJobCategory()
  const sliderValue = useSliderValue()
  const weights = useWeights()
  const setSliderValue = useSetSliderValue()
  const setWeights = useSetWeights()

  // 使用 ref 避免无限循环
  const isInitialMount = useRef(true)

  // 使用防抖避免滑块拖动时的请求风暴
  const debouncedSliderValue = useDebounce(sliderValue, DEBOUNCE_DELAY)

  useEffect(() => {
    // 跳过首次渲染
    if (isInitialMount.current) {
      isInitialMount.current = false
      return
    }

    if (jobCategory) {
      computeWeights(jobCategory, debouncedSliderValue)
        .then(setWeights)
        .catch((error) => console.error('获取权重失败:', error))
    }
  }, [jobCategory, debouncedSliderValue, setWeights])

  const handleSliderChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSliderValue(Number(e.target.value))
  }, [setSliderValue])

  if (!jobCategory) return null

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">调节权重</h3>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          调节滑块 (当前: {sliderValue}%)
        </label>
        <input
          type="range"
          min="0"
          max="50"
          value={sliderValue}
          onChange={handleSliderChange}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
      </div>

      <div className="bg-gray-50 rounded-lg p-3 text-sm">
        <div className="font-medium mb-2">当前评分标准</div>
        <div className="grid grid-cols-2 gap-2 text-gray-600">
          <div>逻辑性: {Math.round(weights.logic * 100)}%</div>
          <div>原则性: {Math.round(weights.principle * 100)}%</div>
          <div>共情力: {Math.round(weights.empathy * 100)}%</div>
          <div>表达力: {Math.round(weights.expression * 100)}%</div>
        </div>
      </div>
    </div>
  )
})
