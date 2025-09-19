"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { WelcomeScreen } from "@/components/welcome-screen"
import { ChatInterface } from "@/components/chat-interface"
import { SubjectSelector } from "@/components/subject-selector"

type View = "welcome" | "subjects" | "chat"

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("welcome")
  const [selectedSubject, setSelectedSubject] = useState<string>("")

  const handleStartChat = (subject?: string) => {
    if (subject) {
      setSelectedSubject(subject)
      setCurrentView("chat")
    } else {
      setCurrentView("subjects")
    }
  }

  const handleSubjectSelect = (subjectId: string) => {
    setSelectedSubject(subjectId)
  }

  const handleStartChatFromSelector = (subjectId: string) => {
    setSelectedSubject(subjectId)
    setCurrentView("chat")
  }

  const handleBackToWelcome = () => {
    setCurrentView("welcome")
    setSelectedSubject("")
  }

  const handleBackToSubjects = () => {
    setCurrentView("subjects")
  }

  const getShowBackButton = () => {
    return currentView === "chat" || currentView === "subjects"
  }

  const getBackClickHandler = () => {
    if (currentView === "chat") {
      return selectedSubject ? handleBackToSubjects : handleBackToWelcome
    }
    return handleBackToWelcome
  }

  return (
    <div className="min-h-screen bg-background">
      <Header
        selectedSubject={selectedSubject}
        onSubjectChange={setSelectedSubject}
        showBackButton={getShowBackButton()}
        onBackClick={getBackClickHandler()}
      />

      <main className="flex-1">
        {currentView === "welcome" && <WelcomeScreen onStartChat={handleStartChat} />}

        {currentView === "subjects" && (
          <div className="container mx-auto px-4 py-8 max-w-4xl">
            <SubjectSelector
              selectedSubject={selectedSubject}
              onSubjectSelect={handleSubjectSelect}
              onStartChat={handleStartChatFromSelector}
            />
          </div>
        )}

        {currentView === "chat" && (
          <ChatInterface selectedSubject={selectedSubject} onSubjectChange={setSelectedSubject} />
        )}
      </main>
    </div>
  )
}
