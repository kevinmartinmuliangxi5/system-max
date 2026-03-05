// useTimer.ts - 计时器 Hook
import { useState, useEffect, useCallback, useRef } from 'react'

// 防抖 Hook - 用于延迟值变化
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])

  return debouncedValue
}

interface UseTimerOptions {
  initialSeconds?: number
  onExpire?: () => void
}

export function useTimer(options: UseTimerOptions = {}) {
  const { initialSeconds = 0, onExpire } = options
  const [seconds, setSeconds] = useState(initialSeconds)
  const [isRunning, setIsRunning] = useState(false)
  const intervalRef = useRef<number | null>(null)
  const onExpireRef = useRef(onExpire)

  // 保持 onExpire 最新
  useEffect(() => {
    onExpireRef.current = onExpire
  }, [onExpire])

  // 计时器逻辑
  useEffect(() => {
    if (isRunning && seconds > 0) {
      intervalRef.current = window.setInterval(() => {
        setSeconds((prev) => {
          if (prev <= 1) {
            setIsRunning(false)
            onExpireRef.current?.()
            return 0
          }
          return prev - 1
        })
      }, 1000)
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isRunning])

  const start = useCallback((duration?: number) => {
    if (duration !== undefined) {
      setSeconds(duration)
    }
    setIsRunning(true)
  }, [])

  const pause = useCallback(() => {
    setIsRunning(false)
  }, [])

  const reset = useCallback((newSeconds?: number) => {
    setIsRunning(false)
    setSeconds(newSeconds ?? initialSeconds)
  }, [initialSeconds])

  const addTime = useCallback((extraSeconds: number) => {
    setSeconds((prev) => prev + extraSeconds)
  }, [])

  // 格式化时间 MM:SS
  const formatted = `${Math.floor(seconds / 60)
    .toString()
    .padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`

  return {
    seconds,
    formatted,
    isRunning,
    start,
    pause,
    reset,
    addTime,
  }
}

// 倒计时专用 Hook
export function useCountdown(duration: number, onExpire?: () => void) {
  const timer = useTimer({ initialSeconds: duration, onExpire })

  const startCountdown = useCallback((newDuration?: number) => {
    const d = newDuration ?? duration
    timer.reset(d)
    timer.start()
  }, [timer, duration])

  return {
    ...timer,
    startCountdown,
    progress: duration > 0 ? ((duration - timer.seconds) / duration) * 100 : 0,
  }
}

// 正计时专用 Hook
export function useStopwatch() {
  const [seconds, setSeconds] = useState(0)
  const [isRunning, setIsRunning] = useState(false)
  const intervalRef = useRef<number | null>(null)

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = window.setInterval(() => {
        setSeconds((prev) => prev + 1)
      }, 1000)
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isRunning])

  const start = useCallback(() => setIsRunning(true), [])
  const pause = useCallback(() => setIsRunning(false), [])
  const reset = useCallback(() => {
    setIsRunning(false)
    setSeconds(0)
  }, [])

  const formatted = `${Math.floor(seconds / 60)
    .toString()
    .padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`

  return { seconds, formatted, isRunning, start, pause, reset }
}
