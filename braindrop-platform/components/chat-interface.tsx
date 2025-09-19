"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Send, Mic, Copy, Brain, User, Loader2, ChevronDown, BookOpen, Clock } from "lucide-react"
import { cn } from "@/lib/utils"
import { useChat, Message } from "@/hooks/use-chat"

interface ChatInterfaceProps {
  selectedSubject: string
  onSubjectChange: (subject: string) => void
}

const subjects = [
  { value: "physics", label: "Physics", labelBn: "পদার্থবিজ্ঞান" },
  { value: "chemistry", label: "Chemistry", labelBn: "রসায়ন" },
  { value: "biology", label: "Biology", labelBn: "জীববিজ্ঞান" },
  { value: "mathematics", label: "Mathematics", labelBn: "গণিত" },
  { value: "general", label: "General Science", labelBn: "সাধারণ বিজ্ঞান" },
]

const quickQuestions = {
  physics: [
    "What is Newton's first law?",
    "Explain electromagnetic induction",
    "How does a transformer work?",
    "What is the photoelectric effect?",
    "What is Ohm's law?",
    "Explain the concept of energy",
    "How do electric circuits work?",
    "What is electromagnetic wave?",
  ],
  chemistry: [
    "What is the periodic table?",
    "Explain chemical bonding",
    "What are acids and bases?",
    "How does photosynthesis work?",
  ],
  biology: [
    "What is cell division?",
    "Explain the circulatory system",
    "How does digestion work?",
    "What is photosynthesis?",
  ],
  mathematics: [
    "Solve quadratic equations",
    "What is trigonometry?",
    "Explain coordinate geometry",
    "How to find derivatives?",
  ],
  general: [
    "What is the scientific method?",
    "Explain the water cycle",
    "What causes seasons?",
    "How do magnets work?",
  ],
}

export function ChatInterface({ selectedSubject, onSubjectChange }: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  
  // Use the custom chat hook
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat({
    includeSources: true,
    searchType: 'hybrid',
    topK: 5
  })

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Clear messages when subject changes
    if (selectedSubject) {
      clearMessages()
    }
  }, [selectedSubject, clearMessages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return
    
    const messageContent = inputValue
    setInputValue("")
    
    await sendMessage(messageContent, selectedSubject)
  }

  const handleQuickQuestion = (question: string) => {
    setInputValue(question)
    inputRef.current?.focus()
  }

  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content)
  }

  const currentQuestions = selectedSubject ? quickQuestions[selectedSubject as keyof typeof quickQuestions] || [] : []

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Sidebar */}
      <div className="hidden lg:flex w-80 border-r border-border bg-muted/30 flex-col">
        <div className="p-4 border-b border-border">
          <h3 className="font-semibold mb-3">Subject</h3>
          <Select value={selectedSubject} onValueChange={onSubjectChange}>
            <SelectTrigger>
              <SelectValue placeholder="Select Subject" />
            </SelectTrigger>
            <SelectContent>
              {subjects.map((subject) => (
                <SelectItem key={subject.value} value={subject.value}>
                  <div className="flex flex-col">
                    <span>{subject.label}</span>
                    <span className="text-xs text-muted-foreground">{subject.labelBn}</span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {selectedSubject && (
          <div className="p-4 flex-1">
            <h3 className="font-semibold mb-3">Quick Questions</h3>
            <div className="space-y-2">
              {currentQuestions.map((question, index) => (
                <Button
                  key={index}
                  variant="ghost"
                  className="w-full justify-start text-left h-auto p-3 text-sm"
                  onClick={() => handleQuickQuestion(question)}
                >
                  {question}
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <Card className="max-w-md">
                <CardContent className="p-6 text-center">
                  <Brain className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">Physics Study Assistant</h3>
                  <p className="text-sm text-muted-foreground mb-3">
                    Ask me anything about physics concepts, problems, or explanations. I have access to your physics textbook content!
                  </p>
                  <p className="text-xs text-muted-foreground">
                    পদার্থবিজ্ঞান সম্পর্কে যেকোনো প্রশ্ন করুন। আমি আপনার পাঠ্যবই থেকে উত্তর দিতে পারি!
                  </p>
                  {error && (
                    <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                      <p className="text-sm text-destructive">{error}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={cn("flex gap-3", message.sender === "user" ? "justify-end" : "justify-start")}
            >
              {message.sender === "ai" && (
                <Avatar className="h-8 w-8 mt-1">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <Brain className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}

              <div
                className={cn(
                  "max-w-[80%] rounded-lg p-4 relative group",
                  message.sender === "user"
                    ? "bg-primary text-primary-foreground ml-12"
                    : "bg-card border border-border",
                )}
              >
                <div className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</div>
                
                {/* Show sources for AI messages */}
                {message.sender === "ai" && message.sources && message.sources.length > 0 && (
                  <Collapsible className="mt-3">
                    <CollapsibleTrigger asChild>
                      <Button variant="ghost" size="sm" className="w-full justify-between p-2 h-auto">
                        <div className="flex items-center gap-2">
                          <BookOpen className="h-4 w-4" />
                          <span className="text-sm">Sources ({message.sources.length})</span>
                        </div>
                        <ChevronDown className="h-4 w-4" />
                      </Button>
                    </CollapsibleTrigger>
                    <CollapsibleContent className="space-y-2 mt-2">
                      {message.sources.map((source, index) => (
                        <div key={index} className="p-3 bg-muted/50 rounded-lg border">
                          <div className="flex items-center gap-2 mb-2">
                            {source.chapter && (
                              <Badge variant="outline" className="text-xs">
                                {source.chapter}
                              </Badge>
                            )}
                            {source.section && (
                              <Badge variant="secondary" className="text-xs">
                                {source.section}
                              </Badge>
                            )}
                            {source.score && (
                              <Badge variant="outline" className="text-xs">
                                {(source.score * 100).toFixed(1)}% match
                              </Badge>
                            )}
                          </div>
                          <p className="text-xs text-muted-foreground line-clamp-3">
                            {source.content}
                          </p>
                        </div>
                      ))}
                    </CollapsibleContent>
                  </Collapsible>
                )}
                
                <div className="flex items-center justify-between mt-2 pt-2 border-t border-border/50">
                  <div className="flex items-center gap-2">
                    <span className="text-xs opacity-70">
                      {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </span>
                    {message.sender === "ai" && (message.searchTime || message.generationTime) && (
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3 opacity-50" />
                        <span className="text-xs opacity-50">
                          {message.searchTime && `${message.searchTime.toFixed(2)}s`}
                          {message.searchTime && message.generationTime && " + "}
                          {message.generationTime && `${message.generationTime.toFixed(2)}s`}
                        </span>
                      </div>
                    )}
                  </div>
                  {message.sender === "ai" && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0"
                      onClick={() => copyMessage(message.content)}
                    >
                      <Copy className="h-3 w-3" />
                    </Button>
                  )}
                </div>
              </div>

              {message.sender === "user" && (
                <Avatar className="h-8 w-8 mt-1">
                  <AvatarFallback className="bg-secondary text-secondary-foreground">
                    <User className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <Avatar className="h-8 w-8 mt-1">
                <AvatarFallback className="bg-primary text-primary-foreground">
                  <Brain className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm text-muted-foreground">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-border p-4">
          {selectedSubject && (
            <div className="mb-3">
              <Badge variant="secondary" className="text-xs">
                {subjects.find((s) => s.value === selectedSubject)?.label} -{" "}
                {subjects.find((s) => s.value === selectedSubject)?.labelBn}
              </Badge>
            </div>
          )}

          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Input
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me anything about your studies... / আপনার পড়াশোনা সম্পর্কে যেকোনো প্রশ্ন করুন..."
                className="pr-12"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault()
                    handleSendMessage()
                  }
                }}
              />
              <Button
                variant="ghost"
                size="sm"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 p-0"
                disabled
              >
                <Mic className="h-4 w-4" />
              </Button>
            </div>
            <Button onClick={handleSendMessage} disabled={!inputValue.trim() || isLoading} className="px-4">
              <Send className="h-4 w-4" />
            </Button>
          </div>

          <p className="text-xs text-muted-foreground mt-2 text-center">
            Press Enter to send • Shift + Enter for new line
          </p>
        </div>
      </div>
    </div>
  )
}
