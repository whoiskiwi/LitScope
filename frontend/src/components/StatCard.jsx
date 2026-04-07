export default function StatCard({ label, value, color = '#4a9eff' }) {
  return (
    <div style={{ background: '#fff', borderRadius: 8, padding: '20px 28px',
      minWidth: 140, boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
      <div style={{ fontSize: 28, fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: 13, color: '#888', marginTop: 4 }}>{label}</div>
    </div>
  )
}
