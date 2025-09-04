import Link from 'next/link'
export default function Home() {
  return (
    <main style={{padding: 24}}>
      <h1>Zentra ASIN Finder</h1>
      <p>Kick off brand coverage runs and share results company-wide.</p>
      <ul>
        <li><Link href="/brands">Brands → Coverage</Link></li>
      </ul>
    </main>
  )
}
