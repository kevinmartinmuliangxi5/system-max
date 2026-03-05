import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Training } from './pages/Training'
import { Exam } from './pages/Exam'
import { ErrorBoundary } from './components/ErrorBoundary'
import { WeightSlider } from './components/WeightSlider'
import { useJobCategory, useSpecificJob, useWeights, useSetJobCategory, useSetSpecificJob, useSetWeights } from './store'
import { getJobs, computeWeights } from './api'
import { useState, useEffect, useCallback, memo } from 'react'
import type { JobInfo, JobCategory } from './types'

// 岗位选择下拉组件
const JobDropdown = memo(function JobDropdown({
  isOpen,
  onClose,
  onSelect
}: {
  isOpen: boolean
  onClose: () => void
  onSelect: (key: JobCategory) => void
}) {
  const [jobs, setJobs] = useState<JobInfo[]>([])

  useEffect(() => {
    if (isOpen) {
      getJobs().then(setJobs).catch(console.error)
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <>
      {/* 背景遮罩 */}
      <div className="fixed inset-0 z-40" onClick={onClose} />

      {/* 下拉菜单 */}
      <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
        {jobs.map((job) => (
          <button
            key={job.key}
            onClick={() => {
              onSelect(job.key as JobCategory)
              onClose()
            }}
            className="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0"
          >
            <div className="font-medium text-gray-800">{job.key}</div>
            <div className="text-xs text-gray-500 mt-0.5">{job.desc}</div>
          </button>
        ))}
      </div>
    </>
  )
})

// 侧边栏组件
function Sidebar() {
  const jobCategory = useJobCategory()
  const specificJob = useSpecificJob()
  const weights = useWeights()
  const setJobCategory = useSetJobCategory()
  const setSpecificJob = useSetSpecificJob()
  const setWeights = useSetWeights()

  const [showJobDropdown, setShowJobDropdown] = useState(false)

  const handleSelectJob = useCallback((key: JobCategory) => {
    setJobCategory(key)
    // 选择岗位后自动获取权重
    computeWeights(key, 0).then(setWeights).catch(console.error)
  }, [setJobCategory, setWeights])

  const navItems = [
    { path: '/training', label: '训练模式' },
    { path: '/exam', label: '模拟考试' },
    { path: '/profile', label: '能力画像' },
  ]

  return (
    <aside className="w-[260px] min-h-screen bg-white border-r border-gray-200 flex flex-col justify-between py-10 px-6">
      {/* 顶部区域 */}
      <div className="space-y-8">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-red-600 rounded flex items-center justify-center">
            <span className="text-white text-lg">🎯</span>
          </div>
          <span className="text-lg font-semibold text-gray-900">公考AI面试官</span>
        </div>

        {/* 导航 */}
        <nav className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-red-50 text-red-600'
                    : 'text-gray-500 hover:bg-gray-50'
                }`
              }
            >
              {item.path === '/training' && (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              )}
              {item.path === '/exam' && (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              {item.path === '/profile' && (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              )}
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* 考生画像配置 */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-gray-900">👤 考生画像配置</h3>

          {/* 岗位类型选择 - 可点击下拉 */}
          <div className="space-y-2">
            <label className="text-xs text-gray-500">岗位类型</label>
            <div className="relative">
              <button
                onClick={() => setShowJobDropdown(!showJobDropdown)}
                className="w-full flex items-center justify-between px-3 py-2.5 border border-gray-200 rounded-md hover:border-gray-300 transition-colors"
              >
                <span className={`text-sm ${jobCategory ? 'text-gray-700' : 'text-gray-400'}`}>
                  {jobCategory || '请选择岗位'}
                </span>
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform ${showJobDropdown ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <JobDropdown
                isOpen={showJobDropdown}
                onClose={() => setShowJobDropdown(false)}
                onSelect={handleSelectJob}
              />
            </div>
          </div>

          {/* 具体岗位输入 */}
          {jobCategory && (
            <div className="space-y-2">
              <label className="text-xs text-gray-500">具体岗位</label>
              <input
                type="text"
                value={specificJob}
                onChange={(e) => setSpecificJob(e.target.value)}
                placeholder="例如：派出所民警"
                className="w-full px-3 py-2 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
              />
            </div>
          )}
        </div>

        {/* 权重调节 */}
        {jobCategory && (
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-900">⚖️ 风格调节</h3>
            <WeightSlider />
          </div>
        )}

        {/* 评分权重 */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-900">📊 评分权重</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-slate-50 rounded-lg p-2.5 text-center">
              <div className="text-xs text-gray-500">逻辑性</div>
              <div className="text-sm font-semibold text-gray-800">{Math.round(weights.logic * 100)}%</div>
            </div>
            <div className="bg-red-50 rounded-lg p-2.5 text-center">
              <div className="text-xs text-gray-500">原则性</div>
              <div className="text-sm font-semibold text-red-600">{Math.round(weights.principle * 100)}%</div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-2.5 text-center">
              <div className="text-xs text-gray-500">共情力</div>
              <div className="text-sm font-semibold text-yellow-600">{Math.round(weights.empathy * 100)}%</div>
            </div>
            <div className="bg-green-50 rounded-lg p-2.5 text-center">
              <div className="text-xs text-gray-500">表达力</div>
              <div className="text-sm font-semibold text-green-600">{Math.round(weights.expression * 100)}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部区域 */}
      <div className="space-y-4">
        {/* 用户信息 */}
        <div className="flex items-center gap-3 pt-3 border-t border-gray-200">
          <div className="w-9 h-9 bg-gray-900 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">考</span>
          </div>
          <div>
            <div className="text-sm font-medium text-gray-900">考生用户</div>
            <div className="text-xs text-gray-500">{specificJob || jobCategory || '未选择岗位'}</div>
          </div>
        </div>
      </div>
    </aside>
  )
}

function AppContent() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 bg-gray-50">
        <Routes>
          <Route path="/" element={<Training />} />
          <Route path="/training" element={<Training />} />
          <Route path="/exam" element={<Exam />} />
          <Route path="/profile" element={<div className="p-10 text-center text-gray-500">能力画像功能开发中...</div>} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
