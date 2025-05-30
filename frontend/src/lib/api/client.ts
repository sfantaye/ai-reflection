// src/lib/api.ts
export async function fetchReflection(entry: string): Promise<string> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080/api/v1'}/reflect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ entry }),
  })

  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`)
  }

  const data = await res.json()
  return data.response
}
