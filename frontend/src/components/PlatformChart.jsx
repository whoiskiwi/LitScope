import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function PlatformChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 0, right: 0, bottom: 40, left: 0 }}>
        <XAxis dataKey="platform" angle={-20} textAnchor="end" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Legend />
        <Bar dataKey="total"      name="Total"       fill="#93c5fd" />
        <Bar dataKey="behavioral" name="Behavioral" fill="#4a9eff" />
      </BarChart>
    </ResponsiveContainer>
  )
}
