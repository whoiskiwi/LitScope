import { useEffect, useState, useRef } from 'react'
import { triggerFetch, triggerClassify, triggerSort, fetchAllJobs, pollJob } from '../api'
import JobStatusBadge from '../components/JobStatusBadge'

const JOB_TYPES = ['fetch', 'classify', 'sort']

export default function JobsPage() {
  const [jobs, setJobs]     = useState({})
  const [error, setError]   = useState('')
  const pollers             = useRef({})

  // Load last known job states on mount
  useEffect(() => {
    fetchAllJobs()
      .then(list => {
        const map = {}
        list.forEach(j => { map[j.job_type] = j })
        setJobs(map)
      })
      .catch(() => {})
  }, [])

  function startPolling(jobType) {
    if (pollers.current[jobType]) return
    pollers.current[jobType] = setInterval(async () => {
      try {
        const state = await pollJob(jobType)
        setJobs(prev => ({ ...prev, [jobType]: state }))
        if (state.status !== 'running') {
          clearInterval(pollers.current[jobType])
          delete pollers.current[jobType]
        }
      } catch {}
    }, 2000)
  }

  async function trigger(fn, jobType) {
    setError('')
    try {
      const res = await fn()
      setJobs(prev => ({ ...prev, [jobType]: res }))
      startPolling(jobType)
    } catch (e) {
      setError(e.message)
    }
  }

  const ACTIONS = [
    { type: 'fetch',    label: 'Fetch new papers',        fn: () => triggerFetch() },
    { type: 'classify', label: 'Classify unclassified',   fn: triggerClassify },
    { type: 'sort',     label: 'Sort & split by platform', fn: triggerSort },
  ]

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Job Management</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {ACTIONS.map(({ type, label, fn }) => {
        const job     = jobs[type]
        const running = job?.status === 'running'
        return (
          <div key={type} style={{ background: '#fff', borderRadius: 8, padding: 20, marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <button
                onClick={() => trigger(fn, type)}
                disabled={running}
                style={{ padding: '8px 20px', cursor: running ? 'not-allowed' : 'pointer',
                  background: '#4a9eff', color: '#fff', border: 'none', borderRadius: 6 }}
              >
                {label}
              </button>
              {job && <JobStatusBadge status={job.status} />}
              {job?.result && <span style={{ color: '#555', fontSize: 14 }}>{job.result}</span>}
            </div>

            {/* Log output */}
            {job?.log?.length > 0 && (
              <pre style={{ background: '#1e2a3a', color: '#a8d8a8', borderRadius: 6,
                padding: 12, fontSize: 12, maxHeight: 200, overflow: 'auto', margin: 0 }}>
                {job.log.join('\n')}
              </pre>
            )}
          </div>
        )
      })}
    </div>
  )
}
