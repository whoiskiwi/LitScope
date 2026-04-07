import { useEffect, useState } from 'react'
import { fetchStats } from '../api'
import StatCard      from '../components/StatCard'
import PlatformChart from '../components/PlatformChart'
import YearChart     from '../components/YearChart'

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
      <h2 style={{ marginTop: 0 }}>Literature Overview</h2>

      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 32 }}>
        <StatCard label="Total Papers"   value={stats.total} />
        <StatCard label="Behavioral"     value={stats.behavioral_count} />
        <StatCard label="Behavioral %"   value={`${stats.behavioral_pct}%`} />
        <StatCard label="Unclassified"   value={stats.unclassified} color="#f59e0b" />
      </div>

      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: 320, background: '#fff', borderRadius: 8, padding: 20 }}>
          <h3 style={{ marginTop: 0 }}>By Platform</h3>
          <PlatformChart data={stats.by_platform} />
        </div>
        <div style={{ flex: 2, minWidth: 400, background: '#fff', borderRadius: 8, padding: 20 }}>
          <h3 style={{ marginTop: 0 }}>Publications by Year</h3>
          <YearChart data={stats.by_year} />
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
