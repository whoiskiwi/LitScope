import { useEffect, useState, useCallback } from 'react'
import { fetchPapers } from '../api'
import FilterBar   from '../components/FilterBar'
import PaperTable  from '../components/PaperTable'
import PaperDetail from '../components/PaperDetail'

export default function BrowsePage() {
  const [filters, setFilters]           = useState({})
  const [result,  setResult]            = useState({ total: 0, data: [] })
  const [page,    setPage]              = useState(1)
  const [loading, setLoading]           = useState(false)
  const [selected, setSelected]         = useState(null)

  const load = useCallback((f, p) => {
    setLoading(true)
    fetchPapers({ ...f, page: p, pageSize: 50 })
      .then(r => { setResult(r); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  useEffect(() => { load(filters, page) }, [filters, page, load])

  function handleFilterChange(f) {
    setFilters(f)
    setPage(1)
  }

  const totalPages = Math.ceil(result.total / 50)

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Browse Papers</h2>
      <FilterBar onChange={handleFilterChange} />

      <div style={{ margin: '12px 0', color: '#666', fontSize: 14 }}>
        {loading ? 'Loading...' : `${result.total} papers found`}
      </div>

      <PaperTable papers={result.data} onSelect={setSelected} />

      {/* Pagination */}
      {totalPages > 1 && (
        <div style={{ marginTop: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
          <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Previous</button>
          <span>{page} / {totalPages}</span>
          <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>Next</button>
        </div>
      )}

      {selected && <PaperDetail paper={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
