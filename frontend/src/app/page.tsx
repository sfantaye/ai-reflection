'use client'

import { useEffect, useState } from 'react'
import { Navbar } from '@/components/navbar'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { fetchReflection } from '@/lib/api/client'
import { Smile, Frown, HelpCircle, Loader2, Send } from 'lucide-react'


export default function Home() {
  const [entry, setEntry] = useState('')
  const [response, setResponse] = useState<{ reflection: string; affirmation: string } | null>(null)
  const [loading, setLoading] = useState(false)
  const [typedReflection, setTypedReflection] = useState('')
  const [typedAffirmation, setTypedAffirmation] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isTypingAffirmation, setIsTypingAffirmation] = useState(false)



const handleSubmit = async () => {
  if (!entry.trim()) return

  setLoading(true)
  setIsTyping(false)
  setIsTypingAffirmation(false)
  setTypedReflection('')
  setTypedAffirmation('')
  setResponse(null)

  try {
    const result = await fetchReflection(entry)
    setResponse(result)
    setIsTyping(true)
  } catch (error) {
    console.error(error)
    setResponse({
      reflection: 'An error occurred.',
      affirmation: 'Please try again later.'
    })
  } finally {
    setLoading(false)
  }
}


useEffect(() => {
  if (response && isTyping) {
    let reflectionIndex = 0
    let affirmationIndex = 0

    const typeReflection = () => {
      if (reflectionIndex <= response.reflection.length) {
        setTypedReflection(response.reflection.slice(0, reflectionIndex))
        reflectionIndex++
        setTimeout(typeReflection, 25)
      } else {
        setIsTyping(false) 
        setIsTypingAffirmation(true)
        setTimeout(typeAffirmation, 500)
      }
    }

    const typeAffirmation = () => {
      if (affirmationIndex <= response.affirmation.length) {
        setTypedAffirmation(response.affirmation.slice(0, affirmationIndex))
        affirmationIndex++
        setTimeout(typeAffirmation, 25)
      } else {
        setIsTypingAffirmation(false) 
      }
    }

    typeReflection()
  }
}, [response, isTyping])







const examplePrompts = [
  {
    id: 'anxious',
    text: 'I’ve been feeling anxious and overwhelmed lately.',
    icon: <Frown className="w-6 h-6 text-orange-500 animate-pulse" />
  },
  {
    id: 'uncertain',
    text: 'I’m not sure if I’m making the right life choices.',
    icon: <HelpCircle className="w-6 h-6 text-yellow-500 animate-bounce" />
  },
  {
    id: 'grateful',
    text: 'I had a great day and want to reflect on it.',
    icon: <Smile className="w-6 h-6 text-green-500 animate-pulse" />
  }
]
  return (
    <main className="flex flex-col min-h-screen bg-background text-foreground">
      <Navbar />

      <div className="flex flex-col flex-grow max-w-2xl mx-auto w-full px-4 pb-4 pt-12">
        {/* Example Prompts */}
       {!response && !loading && !isTyping && !isTypingAffirmation && (
  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6 place-items-center">
    {examplePrompts.map((prompt) => (
      <Card
        key={prompt.id}
        onClick={() => setEntry(prompt.text)}
        className="p-4 text-sm text-center cursor-pointer rounded-xl hover:border-b-orange-500 transition-colors shadow-sm w-full flex flex-col items-center gap-2"
      >
        {prompt.icon}
        <span>{prompt.text}</span>
      </Card>
    ))}
  </div>
)}

        {/* Response Area */}
        {(loading || response) && (
  <div className="flex-grow mb-4 pt-6">
    <Card className="p-6 bg-transparent shadow-none border-none mx-auto">
      <div className="text-center space-y-4">
        <p className="text-lg leading-relaxed text-foreground min-h-[3rem]">
          {typedReflection}
          {(isTyping && !isTypingAffirmation) && (
            <span className="animate-pulse text-orange-500">|</span>
          )}
        </p>

        <p className="text-green-600 font-semibold text-base min-h-[2rem]">
          {typedAffirmation && (
            <>
              <span className="text-orange-400">✨ Affirmation:</span> {typedAffirmation}
              {isTypingAffirmation && <span className="animate-pulse text-orange-500">|</span>}
            </>
          )}
        </p>
      </div>
    </Card>
  </div>
)}


        {/* Input Area */}
<Card className="p-4 border-b-4 border-b-orange-500 shadow-md border rounded-[2em] fixed bottom-6 left-0 right-0 max-w-2xl mx-auto bg-background z-50">
          <div className="flex items-center gap-2">
            <Input
              value={entry}
              onChange={(e) => setEntry(e.target.value)}
              placeholder="How are you feeling today? Type freely..."
              className="flex-1 text-sm placeholder:text-sm px-3 py-10 rounded-xl bg-transparent border-none shadow-none ring-0 focus:outline-none focus:ring-0 focus-visible:ring-0"
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              disabled={loading}
            />
            <Button
              onClick={handleSubmit}
              disabled={loading}
              size="icon"
              className="rounded-2xl bg-orange-500 hover:bg-orange-600 focus:bg-orange-600 active:bg-orange-700 transition-colors disabled:opacity-50 disabled:pointer-events-none"
            >
              {loading ? (
                <Loader2 className="h-10 w-10 animate-spin" />
              ) : (
                <Send className="h-10 w-10" />
              )}
            </Button>
          </div>
        </Card>
      </div>
    </main>
  )
}
