import { useEffect, useState } from 'react'
import { fetchStats } from '../api'

export default function DashboardPage() {
  const [stats, setStats]   = useState(null)
  const [error, setError]   = useState('')

  useEffect(() => {
    fetchStats().then(setStats).catch(e => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'red' }}>{error}</p>
  if (!stats) return <p>Loading...</p>

  return (
    <div>

      {/* Hero: intro left, video right */}
      <div style={{
        display: 'flex', gap: 48, alignItems: 'center',
        flexWrap: 'wrap', marginBottom: 48, paddingBottom: 40,
        borderBottom: '1px solid #e8e8e8',
      }}>
        {/* Left: intro text */}
        <div style={{ flex: 1, minWidth: 260 }}>
          <h1 style={{ fontSize: '2.2rem', lineHeight: 1.2, margin: '0 0 12px' }}>
            Find the Right IS Literature,<br />Faster.
          </h1>
          <p style={{ fontSize: '0.75rem', letterSpacing: '0.12em', color: '#e05a4e',
            textTransform: 'uppercase', fontWeight: 600, margin: '0 0 20px' }}>
            <span>Focused on Information Systems</span>
            <span style={{ display: 'block', marginTop: '4px' }}>
              More Domains Coming Soon...
            </span>
          </p>
          <p style={{ color: '#555', lineHeight: 1.8, margin: '0 0 16px' }}>
            LitScope indexes <strong>{stats.total.toLocaleString()} papers</strong> across top-tier IS journals — MISQ, ISR, and JMIS — and lets you search by theory, topic, or
            natural language query. No more sifting through hundreds of irrelevant
            results. Find TAM studies, UTAUT papers, or privacy-calculus research
            in seconds, with semantic search that understands IS terminology.
          </p>
          <p style={{ color: '#555', lineHeight: 1.8, margin: '0 0 28px' }}>
            Currently, papers are classified by <strong>behavioral theory usage</strong>. Future IS dimensions — including research methodology, technology type, industry context, and theoretical lens — will be added progressively.
            Beyond IS, LitScope will expand to support literature in <strong> other disciplines</strong>, each with domain-specific classification models trained for that field.
          </p>
        </div>

        {/* Right: video */}
        <div style={{ flex: 1.4, minWidth: 300 }}>
          <video
            src="/videos/litscope.mp4"
            controls
            style={{ width: '100%', borderRadius: 6, display: 'block' }}
          />
        </div>
      </div>


      {stats.top_theories.length > 0 && (
        <div style={{ marginTop: 24, background: '#fff', borderRadius: 8, padding: 20 }}>
          <h3 style={{ marginTop: 0 }}>Top 10 Theories</h3>
          {stats.top_theories.map(t => (
            <div key={t.theory} style={{ display: 'flex', justifyContent: 'space-between',
              padding: '6px 0', borderBottom: '1px solid #f0f0f0' }}>
              <span>{t.theory}</span>
              <span style={{ fontWeight: 600, color: '#4a9eff' }}>{t.count}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
