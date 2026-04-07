import { useState, useRef } from 'react'
import { searchPapers }    from '../api'
import PaperDetail         from '../components/PaperDetail'

const EXAMPLE_QUERIES = [
  'Why do users resist adopting new information systems?',
  'How does trust affect online purchase intention?',
  'Social influence and mobile payment adoption',
  'Privacy concerns and information disclosure behavior',
  'Gamification and user motivation in enterprise systems',
]

function ScoreBadge({ score, similarity }) {
  const boost = score - similarity
  return (
    <span style={{ fontSize: 12, color: '#888' }}>
      similarity {similarity.toFixed(3)}
      {boost > 0.001 && (
        <span style={{ color: '#4caf50', marginLeft: 4 }}>
          +{boost.toFixed(3)} boost
        </span>
      )}
    </span>
  )
}

function TheoryTag({ theory }) {
  return (
    <span style={{
      display: 'inline-block',
      background: '#e8f4f8',
      color: '#1a6a8a',
      borderRadius: 4,
      padding: '2px 8px',
      fontSize: 12,
      marginRight: 4,
      marginTop: 4,
    }}>
      {theory}
    </span>
  )
}

function ResultCard({ paper, onSelect }) {
  const theories = paper.theories_used
    ? paper.theories_used.split(',').map(t => t.trim()).filter(Boolean)
    : []

  return (
    <div
      onClick={() => onSelect(paper)}
      style={{
        background: '#fff',
        border: '1px solid #e0e0e0',
        borderRadius: 8,
        padding: '18px 22px',
        marginBottom: 14,
        cursor: 'pointer',
        transition: 'box-shadow 0.15s',
      }}
      onMouseEnter={e => e.currentTarget.style.boxShadow = '0 2px 12px rgba(0,0,0,0.1)'}
      onMouseLeave={e => e.currentTarget.style.boxShadow = 'none'}
    >
      {/* Title row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
        <h4 style={{ margin: 0, fontSize: 15, lineHeight: 1.4, flex: 1 }}>
          {paper.matched_theories?.length > 0 && (
            <span style={{
              background: '#fff3cd',
              color: '#856404',
              fontSize: 11,
              borderRadius: 3,
              padding: '1px 6px',
              marginRight: 8,
              verticalAlign: 'middle',
            }}>
              Theory Match
            </span>
          )}
          {paper.title}
        </h4>
        <span style={{
          fontSize: 12,
          color: paper.is_behavioral ? '#2e7d32' : '#666',
          background: paper.is_behavioral ? '#e8f5e9' : '#f5f5f5',
          borderRadius: 4,
          padding: '2px 8px',
          whiteSpace: 'nowrap',
        }}>
          {paper.is_behavioral ? 'Behavioral' : 'Non-behavioral'}
        </span>
      </div>

      {/* Meta row */}
      <div style={{ marginTop: 6, fontSize: 13, color: '#666', display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        <span>{paper.venue} · {paper.year}</span>
        <ScoreBadge score={paper.score} similarity={paper.similarity} />
      </div>

      {/* Theory tags */}
      {theories.length > 0 && (
        <div style={{ marginTop: 8 }}>
          {theories.map(t => <TheoryTag key={t} theory={t} />)}
        </div>
      )}

      {/* Abstract preview */}
      <p style={{ marginTop: 10, marginBottom: 0, fontSize: 13, color: '#555', lineHeight: 1.6 }}>
        {paper.abstract ? paper.abstract.slice(0, 220) + (paper.abstract.length > 220 ? '…' : '') : ''}
      </p>
    </div>
  )
}

export default function SearchPage() {
  const [query,          setQuery]          = useState('')
  const [onlyBehavioral, setOnlyBehavioral] = useState(false)
  const [topK,           setTopK]           = useState(10)
  const [results,        setResults]        = useState(null)
  const [loading,        setLoading]        = useState(false)
  const [error,          setError]          = useState(null)
  const [selected,       setSelected]       = useState(null)
  const inputRef = useRef(null)

  function handleSearch(q = query) {
    const trimmed = q.trim()
    if (!trimmed) return
    setQuery(trimmed)
    setLoading(true)
    setError(null)
    setResults(null)
    searchPapers({ query: trimmed, topK, onlyBehavioral })
      .then(r  => { setResults(r); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleSearch()
  }

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Semantic Search</h2>
      <p style={{ color: '#666', marginTop: -8, marginBottom: 24 }}>
        Describe what you're looking for in natural language. The system finds papers by meaning, not just keywords.
      </p>

      {/* Search box */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. How does trust affect technology adoption behavior?"
          style={{ flex: 1, padding: '10px 14px', fontSize: 15, borderRadius: 6, border: '1px solid #ccc' }}
        />
        <button
          onClick={() => handleSearch()}
          disabled={loading || !query.trim()}
          style={{ padding: '10px 24px', borderRadius: 6, background: '#1a6a8a', color: '#fff', border: 'none', cursor: 'pointer', fontSize: 15 }}
        >
          {loading ? '...' : 'Search'}
        </button>
      </div>

      {/* Options row */}
      <div style={{ display: 'flex', gap: 24, alignItems: 'center', marginBottom: 20, fontSize: 14 }}>
        <div
          onClick={() => setOnlyBehavioral(v => !v)}
          style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', userSelect: 'none' }}
        >
          <div style={{
            width: 18, height: 18, borderRadius: 4, border: '2px solid #1a6a8a',
            background: onlyBehavioral ? '#1a6a8a' : '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
          }}>
            {onlyBehavioral && <span style={{ color: '#fff', fontSize: 12, lineHeight: 1 }}>✓</span>}
          </div>
          <span>Behavioral</span>
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          Results:
          <select value={topK} onChange={e => setTopK(Number(e.target.value))} style={{ padding: '2px 6px' }}>
            {[5, 10, 20, 30].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>
      </div>

      {/* Example queries */}
      {!results && !loading && (
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 13, color: '#888', marginBottom: 8 }}>Try an example:</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {EXAMPLE_QUERIES.map(q => (
              <button
                key={q}
                onClick={() => { setQuery(q); handleSearch(q) }}
                style={{
                  padding: '5px 12px', borderRadius: 20, border: '1px solid #ccc',
                  background: '#f9f9f9', cursor: 'pointer', fontSize: 13, color: '#444',
                }}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div style={{ textAlign: 'center', padding: 40, color: '#888' }}>
          Searching…
        </div>
      )}

      {/* Error */}
      {error && (
        <div style={{ color: '#c62828', background: '#ffebee', padding: '12px 16px', borderRadius: 6 }}>
          {error}
        </div>
      )}

      {/* Results */}
      {results && (
        <div>
          <div style={{ fontSize: 13, color: '#666', marginBottom: 16 }}>
            {results.results.length} results for <strong>"{results.query}"</strong>
          </div>
          {results.results.map((paper, i) => (
            <ResultCard key={paper.doi || i} paper={paper} onSelect={setSelected} />
          ))}
        </div>
      )}

      {selected && <PaperDetail paper={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
