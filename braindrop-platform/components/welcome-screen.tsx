"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Calculator, Microscope, Atom, Brain, MessageSquare, HelpCircle, Target } from "lucide-react"

const subjects = [
  {
    id: "physics",
    name: "Physics",
    nameBn: "পদার্থবিজ্ঞান",
    icon: Atom,
    color: "bg-blue-500",
    description: "Mechanics, Electricity, Optics",
    descriptionBn: "বলবিদ্যা, বিদ্যুৎ, আলোকবিজ্ঞান",
  },
  {
    id: "chemistry",
    name: "Chemistry",
    nameBn: "রসায়ন",
    icon: Microscope,
    color: "bg-green-500",
    description: "Organic, Inorganic, Physical",
    descriptionBn: "জৈব, অজৈব, ভৌত",
  },
  {
    id: "biology",
    name: "Biology",
    nameBn: "জীববিজ্ঞান",
    icon: BookOpen,
    color: "bg-emerald-500",
    description: "Botany, Zoology, Human Body",
    descriptionBn: "উদ্ভিদবিজ্ঞান, প্রাণিবিজ্ঞান, মানবদেহ",
  },
  {
    id: "mathematics",
    name: "Mathematics",
    nameBn: "গণিত",
    icon: Calculator,
    color: "bg-purple-500",
    description: "Algebra, Geometry, Trigonometry",
    descriptionBn: "বীজগণিত, জ্যামিতি, ত্রিকোণমিতি",
  },
]

const features = [
  {
    icon: MessageSquare,
    title: "Ask Questions",
    titleBn: "প্রশ্ন করুন",
    description: "Get instant answers to your study questions",
    descriptionBn: "আপনার পড়াশোনার প্রশ্নের তাৎক্ষণিক উত্তর পান",
  },
  {
    icon: HelpCircle,
    title: "Get Explanations",
    titleBn: "ব্যাখ্যা পান",
    description: "Understand complex concepts with detailed explanations",
    descriptionBn: "বিস্তারিত ব্যাখ্যার সাথে জটিল ধারণাগুলি বুঝুন",
  },
  {
    icon: Target,
    title: "Practice Problems",
    titleBn: "অনুশীলন সমস্যা",
    description: "Solve practice problems with step-by-step solutions",
    descriptionBn: "ধাপে ধাপে সমাধানের সাথে অনুশীলন সমস্যা সমাধান করুন",
  },
  {
    icon: Brain,
    title: "Smart Learning",
    titleBn: "স্মার্ট শিক্ষা",
    description: "AI-powered personalized learning experience",
    descriptionBn: "AI-চালিত ব্যক্তিগতকৃত শেখার অভিজ্ঞতা",
  },
]

interface WelcomeScreenProps {
  onStartChat: (subject?: string) => void
}

export function WelcomeScreen({ onStartChat }: WelcomeScreenProps) {
  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-primary/20 blur-3xl rounded-full"></div>
            <div className="relative flex h-20 w-20 items-center justify-center rounded-2xl bg-primary">
              <Brain className="h-10 w-10 text-primary-foreground" />
            </div>
          </div>
        </div>

        <h1 className="text-4xl md:text-6xl font-bold mb-4 text-balance">
          Your AI Study Companion
          <br />
          <span className="text-primary">for Class 9-10</span>
        </h1>

        <p className="text-xl text-muted-foreground mb-2 text-pretty">
          Get instant help with Physics, Chemistry, Biology, and Mathematics
        </p>
        <p className="text-lg text-muted-foreground mb-8 text-pretty">ক্লাস ৯-১০ এর জন্য আপনার বুদ্ধিমান পড়াশোনার সাথী</p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" onClick={() => onStartChat()} className="text-lg px-8 py-6">
            Start Learning Now
          </Button>
          <Button size="lg" variant="outline" onClick={() => onStartChat()} className="text-lg px-8 py-6">
            এখনই শুরু করুন
          </Button>
        </div>
      </div>

      {/* Subject Cards */}
      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-center mb-8">Choose Your Subject</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {subjects.map((subject) => {
            const IconComponent = subject.icon
            return (
              <Card
                key={subject.id}
                className="cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-105 group"
                onClick={() => onStartChat(subject.id)}
              >
                <CardHeader className="text-center pb-4">
                  <div className="flex justify-center mb-3">
                    <div className={`p-3 rounded-xl ${subject.color} group-hover:scale-110 transition-transform`}>
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  <CardTitle className="text-lg">{subject.name}</CardTitle>
                  <CardDescription className="text-sm font-medium">{subject.nameBn}</CardDescription>
                </CardHeader>
                <CardContent className="text-center pt-0">
                  <p className="text-sm text-muted-foreground mb-1">{subject.description}</p>
                  <p className="text-xs text-muted-foreground">{subject.descriptionBn}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Features Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-center mb-8">What You Can Do</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const IconComponent = feature.icon
            return (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="flex justify-center mb-3">
                    <div className="p-3 rounded-xl bg-accent">
                      <IconComponent className="h-6 w-6 text-accent-foreground" />
                    </div>
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription className="font-medium">{feature.titleBn}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-2">{feature.description}</p>
                  <p className="text-xs text-muted-foreground">{feature.descriptionBn}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Quick Start Section */}
      <div className="text-center">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle className="text-xl">Ready to Start Learning?</CardTitle>
            <CardDescription>
              Ask me anything about your Class 9-10 studies in English or Bengali
              <br />
              ইংরেজি বা বাংলায় আপনার ক্লাস ৯-১০ পড়াশোনা সম্পর্কে যেকোনো প্রশ্ন করুন
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2 justify-center mb-6">
              <Badge variant="secondary">Instant Answers</Badge>
              <Badge variant="secondary">Step-by-step Solutions</Badge>
              <Badge variant="secondary">Concept Explanations</Badge>
              <Badge variant="secondary">Practice Problems</Badge>
            </div>
            <Button size="lg" onClick={() => onStartChat()} className="w-full sm:w-auto">
              Start Your First Question
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
