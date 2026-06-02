import { useState, useRef, useEffect, useCallback } from 'react'
import { Send, Bot, User, Loader2, Sparkles, RotateCcw, Zap, AlignLeft } from 'lucide-react'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const INITIAL_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  content: 'Olá! Sou o **Nexus**, seu assistente com RAG e MCP. Como posso ajudar você hoje?',
}

function MessageBubble({ message, isStreaming }) {
  const isUser = message.role === 'user'
  const isLastAssistant = !isUser && isStreaming && message.content !== undefined

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 ${
          isUser
            ? 'bg-violet-600'
            : 'bg-gradient-to-br from-blue-500 to-violet-600'
        }`}
      >
        {isUser ? <User size={14} /> : <Bot size={14} />}
      </div>

      <div
        className={`max-w-[78%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-violet-600 text-white rounded-tr-sm'
            : 'bg-gray-800 text-gray-100 rounded-tl-sm'
        }`}
      >
        <span className="whitespace-pre-wrap">{message.content}</span>
        {isLastAssistant && (
          <span className="inline-block w-[2px] h-4 ml-0.5 bg-gray-400 animate-pulse align-middle" />
        )}
      </div>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-4 text-center px-6">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
        <Sparkles size={28} className="text-white" />
      </div>
      <div>
        <h2 className="text-xl font-semibold text-white">Nexus</h2>
        <p className="text-gray-400 text-sm mt-1">AI · RAG · MCP · Document Ingestion</p>
      </div>
      <p className="text-gray-500 text-sm max-w-sm">
        Faça uma pergunta para começar. O assistente busca na base de conhecimento e responde com IA.
      </p>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([INITIAL_MESSAGE])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamMode, setStreamMode] = useState(true)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const abortRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = useCallback(async (e) => {
    e?.preventDefault()
    const question = input.trim()
    if (!question || isStreaming) return

    const userMsg = { id: `u-${Date.now()}`, role: 'user', content: question }
    const assistantMsg = { id: `a-${Date.now()}`, role: 'assistant', content: '' }

    setMessages((prev) => [...prev, userMsg, assistantMsg])
    setInput('')
    setIsStreaming(true)

    const controller = new AbortController()
    abortRef.current = controller

    try {
      if (streamMode) {
        const response = await fetch(`${BACKEND_URL}/ask/stream`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question }),
          signal: controller.signal,
        })

        if (!response.ok) throw new Error(`HTTP ${response.status}`)

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''
        let acc = '' 

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            const data = line.slice(6).trim()
            if (data === '[DONE]') continue

            try {
              const { token } = JSON.parse(data)
              if (token) acc += token
            } catch {}
          }

          setMessages((prev) => {
            const updated = [...prev]
            const last = { ...updated[updated.length - 1] }
            last.content = acc
            updated[updated.length - 1] = last
            return updated
          })
        }
      } else {
        const response = await fetch(`${BACKEND_URL}/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question }),
          signal: controller.signal,
        })

        if (!response.ok) throw new Error(`HTTP ${response.status}`)

        const { answer } = await response.json()
        setMessages((prev) => {
          const updated = [...prev]
          const last = { ...updated[updated.length - 1] }
          last.content = answer
          updated[updated.length - 1] = last
          return updated
        })
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setMessages((prev) => {
          const updated = [...prev]
          const last = { ...updated[updated.length - 1] }
          last.content = 'Erro ao conectar com o servidor. Verifique se o backend está rodando.'
          updated[updated.length - 1] = last
          return updated
        })
      }
    } finally {
      setIsStreaming(false)
      abortRef.current = null
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }, [input, isStreaming, streamMode])

  const handleClear = () => {
    if (isStreaming) abortRef.current?.abort()
    setMessages([INITIAL_MESSAGE])
    setIsStreaming(false)
    setTimeout(() => inputRef.current?.focus(), 50)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="flex items-center justify-between px-5 py-3 border-b border-gray-800 bg-gray-900 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-white text-sm leading-none">Nexus</h1>
            <p className="text-xs text-gray-500 mt-0.5">AI · RAG · MCP</p>
          </div>
        </div>

        <button
          onClick={handleClear}
          title="Nova conversa"
          className="w-8 h-8 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 flex items-center justify-center transition-colors"
        >
          <RotateCcw size={15} />
        </button>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 1 && messages[0].id === 'welcome' ? (
          <EmptyState />
        ) : (
          <div className="max-w-3xl mx-auto space-y-5">
            {messages.map((msg) => (
              <MessageBubble
                key={msg.id}
                message={msg}
                isStreaming={isStreaming && msg.id === messages[messages.length - 1]?.id}
              />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div className="shrink-0 border-t border-gray-800 bg-gray-900 px-4 pb-5 pt-3">
        <form
          onSubmit={handleSubmit}
          className="flex gap-3 items-end max-w-3xl mx-auto"
        >
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua mensagem..."
            rows={1}
            disabled={isStreaming}
            className="flex-1 bg-gray-800 border border-gray-700 focus:border-violet-500 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 resize-none focus:outline-none transition-colors disabled:opacity-50 min-h-[44px] max-h-[120px] overflow-y-auto"
          />
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="w-11 h-11 rounded-xl bg-violet-600 hover:bg-violet-500 disabled:bg-gray-700 disabled:cursor-not-allowed flex items-center justify-center transition-colors shrink-0"
          >
            {isStreaming
              ? <Loader2 size={18} className="animate-spin" />
              : <Send size={17} />
            }
          </button>
        </form>
        <div className="flex items-center justify-between max-w-3xl mx-auto mt-2 px-1">
          <p className="text-xs text-gray-700">
            Enter para enviar · Shift+Enter para nova linha
          </p>
          <button
            type="button"
            onClick={() => setStreamMode((v) => !v)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
              streamMode
                ? 'bg-violet-600/20 text-violet-400 hover:bg-violet-600/30'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {streamMode ? <Zap size={12} /> : <AlignLeft size={12} />}
            {streamMode ? 'Stream' : 'Completo'}
          </button>
        </div>
      </div>
    </div>
  )
}
