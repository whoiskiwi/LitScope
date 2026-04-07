import { useState, useEffect, useRef } from 'react'

const PLATFORMS = [
  '',
  'INFORMS / ISR',
  'AIS / MISQ',
  'Taylor & Francis / JMIS',
]

export default function FilterBar({ onChange }) {
  const [platform,     setPlatform]     = useState('')
  const [yearMin,      setYearMin]      = useState('')
  const [yearMax,      setYearMax]      = useState('')
  const [isBehavioral, setIsBehavioral] = useState('')
  const [keyword,      setKeyword]      = useState('')
  const debounce = useRef(null)

  function emit(overrides = {}) {
    const f = {
      platform:      (overrides.platform     ?? platform)     || undefined,
      yearMin:       (overrides.yearMin       ?? yearMin)      || undefined,
      yearMax:       (overrides.yearMax       ?? yearMax)      || undefined,
      isBehavioral:  overrides.isBehavioral   ?? (isBehavioral === '' ? undefined : isBehavioral === 'true'),
      keyword:       (overrides.keyword       ?? keyword)      || undefined,
    }
    onChange(f)
  }

  function handleKeyword(v) {
    setKeyword(v)
    clearTimeout(debounce.current)
    debounce.current = setTimeout(() => emit({ keyword: v || undefined }), 350)
  }

  const sel = { padding: '6px 10px', borderRadius: 6, border: '1px solid #ddd', fontSize: 13 }
  const inp = { ...sel, width: 72 }

  return (
    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center',
      background: '#fff', padding: '12px 16px', borderRadius: 8 }}>

      <select style={sel} value={platform} onChange={e => { setPlatform(e.target.value); emit({ platform: e.target.value || undefined }) }}>
        {PLATFORMS.map(p => <option key={p} value={p}>{p || 'All platforms'}</option>)}
      </select>

      <input style={inp} type="number" placeholder="Year from" value={yearMin}
        onChange={e => { setYearMin(e.target.value); emit({ yearMin: e.target.value || undefined }) }} />
      <span style={{ color: '#999' }}>—</span>
      <input style={inp} type="number" placeholder="Year to" value={yearMax}
        onChange={e => { setYearMax(e.target.value); emit({ yearMax: e.target.value || undefined }) }} />

      <select style={sel} value={isBehavioral} onChange={e => { setIsBehavioral(e.target.value); emit({ isBehavioral: e.target.value }) }}>
        <option value="">All types</option>
        <option value="true">Behavioral</option>
        <option value="false">Non-behavioral</option>
      </select>

      <input style={{ ...inp, width: 200 }} type="text" placeholder="Search title / abstract..."
        value={keyword} onChange={e => handleKeyword(e.target.value)} />
    </div>
  )
}
