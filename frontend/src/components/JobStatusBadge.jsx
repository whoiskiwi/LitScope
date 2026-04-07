const STYLE = {
  running: { bg: '#fef3c7', color: '#92400e', text: 'Running...' },
  done:    { bg: '#d1fae5', color: '#065f46', text: 'Done' },
  error:   { bg: '#fee2e2', color: '#991b1b', text: 'Error' },
}

export default function JobStatusBadge({ status }) {
  const s = STYLE[status] || { bg: '#f3f4f6', color: '#6b7280', text: status }
  return (
    <span style={{ background: s.bg, color: s.color,
      padding: '3px 12px', borderRadius: 12, fontSize: 13, fontWeight: 500 }}>
      {s.text}
    </span>
  )
}
