export interface ReflectionResult {
  reflection: string;
  affirmation: string;
  follow_ups?: string[]; 
}

export async function fetchReflection(entry: string): Promise<ReflectionResult> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080'}/reflect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ entry }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }

  const data = await res.json();

  return {
    reflection: data.reflection,
    affirmation: data.affirmation,
    follow_ups: data.follow_ups ?? [], 
  };
}
