/**
 * api.js — All backend requests are centralized here; components never construct URLs directly
 */

const BASE = import.meta.env.VITE_API_URL || ''

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Papers ─────────────────────────────────────────────────────────────────
export function fetchPapers({ platform, yearMin, yearMax, isBehavioral, keyword, page = 1, pageSize = 50 } = {}) {
  const params = new URLSearchParams()
  if (platform      != null) params.set('platform',      platform)
  if (yearMin       != null) params.set('year_min',       yearMin)
  if (yearMax       != null) params.set('year_max',       yearMax)
  if (isBehavioral  != null) params.set('is_behavioral',  isBehavioral)
  if (keyword             ) params.set('keyword',        keyword)
  params.set('page',      page)
  params.set('page_size', pageSize)
  return request(`/api/papers?${params}`)
}

export function fetchPaperByDoi(doi) {
  return request(`/api/papers/${encodeURIComponent(doi)}`)
}

// ── Stats ──────────────────────────────────────────────────────────────────
export function fetchStats() {
  return request('/api/stats')
}

// ── Jobs ───────────────────────────────────────────────────────────────────
export function triggerFetch(journals = null) {
  return request('/api/jobs/fetch', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ journals }),
  })
}

export function triggerClassify() {
  return request('/api/jobs/classify', { method: 'POST' })
}

export function triggerSort() {
  return request('/api/jobs/sort', { method: 'POST' })
}

export function fetchAllJobs() {
  return request('/api/jobs')
}

export function pollJob(jobType) {
  return request(`/api/jobs/${jobType}`)
}

// ── Search ─────────────────────────────────────────────────────────────────
export function searchPapers({ query, topK = 10, onlyBehavioral = false } = {}) {
  const params = new URLSearchParams()
  params.set('q',               query)
  params.set('top_k',           topK)
  params.set('only_behavioral', onlyBehavioral)
  return request(`/api/search?${params}`)
}
