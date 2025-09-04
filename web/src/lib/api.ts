export async function runCoverage(brand: string, opts?: { bsrMax?: number; requireBuybox?: boolean }) {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const resp = await fetch(`${api}/brands/coverage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ brand, bsr_max: opts?.bsrMax ?? 250000, require_buybox: opts?.requireBuybox ?? true })
  });
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}
