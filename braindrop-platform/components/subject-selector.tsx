"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Calculator, Microscope, Atom, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

const subjects = [
  {
    id: "physics",
    name: "Physics",
    nameBn: "পদার্থবিজ্ঞান",
    icon: Atom,
    color: "bg-blue-500",
    description: "Mechanics, Electricity, Optics, Modern Physics",
    descriptionBn: "বলবিদ্যা, বিদ্যুৎ, আলোকবিজ্ঞান, আধুনিক পদার্থবিজ্ঞান",
    topics: ["Newton's Laws", "Electromagnetic Induction", "Wave Optics", "Atomic Structure"],
    topicsBn: ["নিউটনের সূত্র", "তড়িৎচুম্বকীয় আবেশ", "তরঙ্গ আলোকবিজ্ঞান", "পরমাণুর গঠন"],
  },
  {
    id: "chemistry",
    name: "Chemistry",
    nameBn: "রসায়ন",
    icon: Microscope,
    color: "bg-green-500",
    description: "Organic, Inorganic, Physical Chemistry",
    descriptionBn: "জৈব, অজৈব, ভৌত রসায়ন",
    topics: ["Chemical Bonding", "Acids & Bases", "Organic Compounds", "Periodic Table"],
    topicsBn: ["রাসায়নিক বন্ধন", "অ্যাসিড ও ক্ষার", "জৈব যৌগ", "পর্যায় সারণি"],
  },
  {
    id: "biology",
    name: "Biology",
    nameBn: "জীববিজ্ঞান",
    icon: BookOpen,
    color: "bg-emerald-500",
    description: "Botany, Zoology, Human Physiology",
    descriptionBn: "উদ্ভিদবিজ্ঞান, প্রাণিবিজ্ঞান, মানব শরীরতত্ত্ব",
    topics: ["Cell Biology", "Genetics", "Evolution", "Ecology"],
    topicsBn: ["কোষবিজ্ঞান", "বংশগতিবিদ্যা", "বিবর্তন", "বাস্তুবিদ্যা"],
  },
  {
    id: "mathematics",
    name: "Mathematics",
    nameBn: "গণিত",
    icon: Calculator,
    color: "bg-purple-500",
    description: "Algebra, Geometry, Trigonometry, Statistics",
    descriptionBn: "বীজগণিত, জ্যামিতি, ত্রিকোণমিতি, পরিসংখ্যান",
    topics: ["Quadratic Equations", "Coordinate Geometry", "Trigonometry", "Probability"],
    topicsBn: ["দ্বিঘাত সমীকরণ", "স্থানাঙ্ক জ্যামিতি", "ত্রিকোণমিতি", "সম্ভাব্যতা"],
  },
]

interface SubjectSelectorProps {
  selectedSubject: string
  onSubjectSelect: (subjectId: string) => void
  onStartChat: (subjectId: string) => void
}

export function SubjectSelector({ selectedSubject, onSubjectSelect, onStartChat }: SubjectSelectorProps) {
  const [hoveredSubject, setHoveredSubject] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold mb-2">Choose Your Subject</h2>
        <p className="text-muted-foreground">আপনার বিষয় নির্বাচন করুন</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {subjects.map((subject) => {
          const IconComponent = subject.icon
          const isSelected = selectedSubject === subject.id
          const isHovered = hoveredSubject === subject.id

          return (
            <Card
              key={subject.id}
              className={cn(
                "cursor-pointer transition-all duration-300 hover:shadow-lg group relative overflow-hidden",
                isSelected && "ring-2 ring-primary shadow-lg",
                isHovered && "scale-[1.02]",
              )}
              onMouseEnter={() => setHoveredSubject(subject.id)}
              onMouseLeave={() => setHoveredSubject(null)}
              onClick={() => onSubjectSelect(subject.id)}
            >
              <div className={cn("absolute inset-0 opacity-0 transition-opacity", isHovered && "opacity-5")}>
                <div className={cn("w-full h-full", subject.color)} />
              </div>

              <CardHeader className="relative">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={cn("p-3 rounded-xl transition-transform", subject.color, isHovered && "scale-110")}>
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{subject.name}</CardTitle>
                      <CardDescription className="font-medium">{subject.nameBn}</CardDescription>
                    </div>
                  </div>
                  {isSelected && <Badge variant="default">Selected</Badge>}
                </div>
              </CardHeader>

              <CardContent className="relative space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">{subject.description}</p>
                  <p className="text-xs text-muted-foreground">{subject.descriptionBn}</p>
                </div>

                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Key Topics:</h4>
                  <div className="grid grid-cols-2 gap-1">
                    {subject.topics.slice(0, 4).map((topic, index) => (
                      <div key={index} className="text-xs">
                        <span className="text-muted-foreground">• {topic}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <Button
                    variant={isSelected ? "default" : "outline"}
                    size="sm"
                    className="flex-1"
                    onClick={(e) => {
                      e.stopPropagation()
                      onSubjectSelect(subject.id)
                    }}
                  >
                    {isSelected ? "Selected" : "Select"}
                  </Button>
                  <Button
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation()
                      onStartChat(subject.id)
                    }}
                    className="flex items-center gap-1"
                  >
                    Start
                    <ChevronRight className="h-3 w-3" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {selectedSubject && (
        <div className="text-center">
          <Button size="lg" onClick={() => onStartChat(selectedSubject)} className="px-8">
            Start Learning {subjects.find((s) => s.id === selectedSubject)?.name}
          </Button>
        </div>
      )}
    </div>
  )
}
