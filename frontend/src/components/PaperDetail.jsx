function platformUrl(platform, doi) {
  if (!doi) return '#'
  return `https://doi.org/${doi}`
}

export default function PaperDetail({ paper, onClose }) {
  if (!paper) return null

  return (
    <div onClick={onClose}
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.45)', zIndex: 1000,
        display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div onClick={e => e.stopPropagation()}
        style={{ background: '#fff', borderRadius: 12, padding: 32, maxWidth: 700,
          width: '90%', maxHeight: '85vh', overflowY: 'auto', boxShadow: '0 20px 60px rgba(0,0,0,0.3)' }}>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <h3 style={{ margin: '0 16px 0 0', lineHeight: 1.4 }}>{paper.title}</h3>
          <button onClick={onClose} style={{ border: 'none', background: 'none',
            fontSize: 22, cursor: 'pointer', color: '#999', flexShrink: 0 }}>✕</button>
        </div>

        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', margin: '12px 0' }}>
          <Tag label={paper.platform} />
          <Tag label={paper.year} />
          <Tag label={paper.is_behavioral ? '✅ Behavioral' : '❌ Non-behavioral'}
               color={paper.is_behavioral ? '#065f46' : '#6b7280'}
               bg={paper.is_behavioral ? '#d1fae5' : '#f3f4f6'} />
          {paper.confidence && <Tag label={`Confidence: ${paper.confidence}`} />}
        </div>

        {paper.authors && <p style={{ color: '#555', fontSize: 13, margin: '8px 0' }}>
          <b>Authors: </b>{paper.authors}
        </p>}

        {paper.theories_used && (
          <p style={{ color: '#555', fontSize: 13, margin: '8px 0' }}>
            <b>Theories: </b>{paper.theories_used}
          </p>
        )}

        {paper.reason && (
          <p style={{ color: '#555', fontSize: 13, margin: '8px 0' }}>
            <b>Classification reason: </b>{paper.reason}
          </p>
        )}

        {paper.abstract && (
          <div style={{ marginTop: 16 }}>
            <b style={{ fontSize: 13 }}>Abstract</b>
            <p style={{ fontSize: 13, lineHeight: 1.7, color: '#444', marginTop: 8 }}>{paper.abstract}</p>
          </div>
        )}

        {paper.doi && (
          <p style={{ fontSize: 12, marginTop: 16 }}>
            <b>DOI: </b>
            <a
              href={platformUrl(paper.platform, paper.doi)}
              target="_blank"
              rel="noreferrer"
              style={{ color: '#4a9eff' }}
            >
              {paper.doi}
            </a>
          </p>
        )}
      </div>
    </div>
  )
}

function Tag({ label, color = '#374151', bg = '#e5e7eb' }) {
  return (
    <span style={{ background: bg, color, padding: '2px 10px', borderRadius: 12, fontSize: 12 }}>
      {label}
    </span>
  )
}
