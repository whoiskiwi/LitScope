const BADGE = {
  true:  { bg: '#d1fae5', color: '#065f46', text: 'Behavioral' },
  false: { bg: '#f3f4f6', color: '#6b7280', text: 'Non-behavioral' },
}

export default function PaperTable({ papers, onSelect }) {
  if (!papers.length) return <p style={{ color: '#999' }}>No papers match the current filters.</p>

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        <thead>
          <tr style={{ background: '#f0f4f8', textAlign: 'left' }}>
            {['Title', 'Year', 'Platform', 'Type', 'Confidence'].map(h => (
              <th key={h} style={{ padding: '10px 12px', fontWeight: 600 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {papers.map((p, i) => {
            const badge = BADGE[String(p.is_behavioral)] || { bg: '#fff7ed', color: '#92400e', text: '?' }
            return (
              <tr key={i}
                onClick={() => onSelect(p)}
                style={{ cursor: 'pointer', borderBottom: '1px solid #eee',
                  background: i % 2 === 0 ? '#fff' : '#fafafa' }}
                onMouseEnter={e => e.currentTarget.style.background = '#eff6ff'}
                onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? '#fff' : '#fafafa'}
              >
                <td style={{ padding: '10px 12px', maxWidth: 400 }}>
                  <span title={p.title}>{p.title?.slice(0, 80)}{p.title?.length > 80 ? '…' : ''}</span>
                </td>
                <td style={{ padding: '10px 12px', whiteSpace: 'nowrap' }}>{p.year}</td>
                <td style={{ padding: '10px 12px', whiteSpace: 'nowrap', color: '#555' }}>{p.platform}</td>
                <td style={{ padding: '10px 12px' }}>
                  <span style={{ background: badge.bg, color: badge.color,
                    padding: '2px 8px', borderRadius: 12, fontSize: 12 }}>{badge.text}</span>
                </td>
                <td style={{ padding: '10px 12px', color: '#888' }}>{p.confidence}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
