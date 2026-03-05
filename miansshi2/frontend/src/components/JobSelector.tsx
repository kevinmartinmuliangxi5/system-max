// JobSelector.tsx - 岗位选择组件
import { useJobCategory, useSpecificJob, useSetJobCategory, useSetSpecificJob } from '../store'
import { getJobs } from '../api'
import { useEffect, useState, useCallback, memo } from 'react'
import type { JobInfo } from '../types'

export const JobSelector = memo(function JobSelector() {
  const jobCategory = useJobCategory()
  const specificJob = useSpecificJob()
  const setJobCategory = useSetJobCategory()
  const setSpecificJob = useSetSpecificJob()
  const [jobs, setJobs] = useState<JobInfo[]>([])

  useEffect(() => {
    getJobs().then(setJobs).catch(console.error)
  }, [])

  const handleSelectJob = useCallback((key: string) => {
    setJobCategory(key as any)
  }, [setJobCategory])

  const handleSpecificJobChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSpecificJob(e.target.value)
  }, [setSpecificJob])

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">选择岗位类型</h3>

      <div className="space-y-2">
        {jobs.map((job) => (
          <button
            key={job.key}
            onClick={() => handleSelectJob(job.key)}
            className={`w-full text-left p-3 rounded-lg border-2 transition-all ${
              jobCategory === job.key
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="font-medium">{job.key}</div>
            <div className="text-sm text-gray-500">{job.desc}</div>
          </button>
        ))}
      </div>

      {jobCategory && (
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            具体岗位名称
          </label>
          <input
            type="text"
            value={specificJob}
            onChange={handleSpecificJobChange}
            placeholder="例如：派出所民警"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      )}
    </div>
  )
})
