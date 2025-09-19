"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { ArrowLeft, Brain, Moon, Sun } from "lucide-react"

const subjects = [
  { value: "physics", label: "Physics", labelBn: "পদার্থবিজ্ঞান" },
  { value: "chemistry", label: "Chemistry", labelBn: "রসায়ন" },
  { value: "biology", label: "Biology", labelBn: "জীববিজ্ঞান" },
  { value: "mathematics", label: "Mathematics", labelBn: "গণিত" },
  { value: "general", label: "General Science", labelBn: "সাধারণ বিজ্ঞান" },
]

interface HeaderProps {
  selectedSubject: string
  onSubjectChange: (subject: string) => void
  showBackButton?: boolean
  onBackClick?: () => void
}

export function Header({ selectedSubject, onSubjectChange, showBackButton = false, onBackClick }: HeaderProps) {
  const [isDark, setIsDark] = useState(false)

  const toggleTheme = () => {
    setIsDark(!isDark)
    document.documentElement.classList.toggle("dark")
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center justify-between px-4">
        <div className="flex items-center gap-4">
          {showBackButton && (
            <Button variant="ghost" size="sm" onClick={onBackClick} className="flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              <span className="hidden sm:inline">Back</span>
            </Button>
          )}

          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Brain className="h-5 w-5 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-lg font-semibold leading-none">Braindrop</h1>
              <p className="text-xs text-muted-foreground">AI Study Companion</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex">
            <Select value={selectedSubject} onValueChange={onSubjectChange}>
              <SelectTrigger className="w-48">
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

          <Button variant="ghost" size="sm" onClick={toggleTheme} className="h-9 w-9 p-0">
            {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>

          <Avatar className="h-8 w-8">
            <AvatarFallback className="bg-primary text-primary-foreground text-sm">S</AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  )
}
