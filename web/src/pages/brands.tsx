import { useState } from 'react'
import { runCoverage } from '../lib/api'

export default function Brands() {
  const [brand, setBrand] = useState('Bernette')
  const [rows, setRows] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onRun() {
    try {
      setLoading(true); setError(null)
      const data = await runCoverage(brand, { bsrMax: 250000, requireBuybox: true })
      setRows(data.asins)
    } catch (e:any) {
      setError(e.message)
    } finally { setLoading(false) }
  }

  return (
    <main style={{padding: 24}}>
      <h2>Brand Coverage</h2>
      <div style={{display:'flex', gap:8, margin:'12px 0'}}>
        <input value={brand} onChange={e=>setBrand(e.target.value)} placeholder="Brand name" />
        <button onClick={onRun} disabled={loading}>{loading? 'Running…':'Run coverage'}</button>
      </div>
      {error && <p style={{color:'crimson'}}>{error}</p>}
      <p>Showing first {rows.length} ASINs.</p>
      <div style={{maxHeight: 400, overflow:'auto', border:'1px solid #ddd'}}>
        <table width="100%">
          <thead><tr><th>#</th><th>ASIN</th></tr></thead>
          <tbody>
            {rows.map((a, i)=> (
              <tr key={a}><td>{i+1}</td><td>{a}</td></tr>
            ))}
          </tbody>
        </table>

      </div>
    </main>
  )
}
