
"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { LogOut, FileText, MapPin, Mail, Phone, Download, Edit, Printer } from "lucide-react"

interface UserProfile {
  user_id?: number
  name: string
  email: string
  age?: number
  location?: string
  bio?: string
  github?: string
  linkedin?: string
  huggingface?: string
  x?: string
  website?: string
  skills?: string[]
  certifications?: string[]
  projects?: any[]
  blogs?: any[]
  achievements?: string[]
  profile_completeness?: number
}

export  default function DashboardPage() {
  const router = useRouter()
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    // Check if user has completed registration
    const storedProfile = localStorage.getItem("userProfile")
    if (!storedProfile) {
      router.push("/register")
      return
    }

    try {
      const profile = JSON.parse(storedProfile)
      console.log("Loaded profile:", profile) // Debug log
      setUserProfile(profile)
    } catch (error) {
      console.error("Error parsing stored profile:", error)
      router.push("/register")
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem("userProfile")
    router.push("/")
  }

  // Helper function to split name
  const getFirstName = (fullName: string) => {
    return fullName ? fullName.split(' ')[0] : 'User'
  }

  const getLastName = (fullName: string) => {
    const parts = fullName ? fullName.split(' ') : []
    return parts.length > 1 ? parts.slice(1).join(' ') : ''
  }

  // Helper function to determine experience level
  const getExperienceLevel = (profile: UserProfile) => {
    const skillsCount = profile.skills?.length || 0
    const projectsCount = profile.projects?.length || 0
    
    if (skillsCount >= 8 && projectsCount >= 5) return 'senior level'
    if (skillsCount >= 5 && projectsCount >= 3) return 'mid level'
    return 'entry level'
  }

  if (!userProfile) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  const firstName = getFirstName(userProfile.name)
  const lastName = getLastName(userProfile.name)
  const experienceLevel = getExperienceLevel(userProfile)

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b-2 border-slate-800 bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded bg-slate-800 text-white">
                  <FileText className="h-5 w-5" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900" style={{ fontFamily: "Georgia, serif" }}>
                    Professional Resume
                  </h1>
                  <p className="text-sm text-slate-600">Digital Career Document</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                className="border-slate-300 text-slate-700 hover:bg-slate-50 bg-transparent"
              >
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="border-slate-300 text-slate-700 hover:bg-slate-50 bg-transparent"
              >
                <Printer className="h-4 w-4 mr-2" />
                Print
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="border-slate-300 text-slate-700 hover:bg-slate-50 bg-transparent"
              >
                <Edit className="h-4 w-4 mr-2" />
                Edit
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Exit
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto bg-white shadow-lg border border-slate-200 my-8">
        <div className="p-12" style={{ fontFamily: "Georgia, serif" }}>
          <header className="text-center border-b-4 border-slate-800 pb-8 mb-10">
            <h1
              className="text-5xl font-bold text-slate-900 mb-3 tracking-tight"
              style={{ fontFamily: "Georgia, serif" }}
            >
              {firstName} {lastName}
            </h1>
            <h2 className="text-2xl text-slate-700 font-normal mb-6 italic">
              {experienceLevel.charAt(0).toUpperCase() + experienceLevel.slice(1)} Developer
            </h2>
            <div className="flex flex-wrap justify-center gap-8 text-slate-600">
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                <span>{userProfile.email}</span>
              </div>
              {userProfile.age && (
                <div className="flex items-center gap-2">
                  <span>Age: {userProfile.age}</span>
                </div>
              )}
              {userProfile.location && (
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  <span>{userProfile.location}</span>
                </div>
              )}
            </div>
          </header>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-4 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Professional Summary
            </h3>
            <p className="text-slate-700 leading-relaxed text-lg">
              {userProfile.bio ||
                `Accomplished developer with ${experienceLevel} experience in technology solutions. Demonstrated expertise in modern development practices and delivering scalable applications. Passionate about innovation and committed to excellence in every project.`}
            </p>
          </section>

          {userProfile.skills && userProfile.skills.length > 0 && (
            <section className="mb-10">
              <h3 className="text-xl font-bold text-slate-900 mb-4 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
                Core Competencies
              </h3>
              <div className="grid grid-cols-4 gap-4">
                {userProfile.skills.map((skill, index) => (
                  <div key={index} className="text-slate-700 font-medium">
                    • {skill}
                  </div>
                ))}
              </div>
            </section>
          )}

          {userProfile.projects && userProfile.projects.length > 0 && (
            <section className="mb-10">
              <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
                Key Projects
              </h3>
              <div className="space-y-6">
                {userProfile.projects.map((project, index) => (
                  <div key={index}>
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="text-lg font-bold text-slate-900">{project.title}</h4>
                      <span className="text-slate-600 font-medium">2024</span>
                    </div>
                    {project.technologies && (
                      <p className="text-slate-600 text-sm mb-2 italic">{project.technologies}</p>
                    )}
                    <p className="text-slate-700">{project.description}</p>
                    {project.link && (
                      <p className="text-slate-600 text-sm mt-1">
                        <a href={project.link} className="underline">View Project</a>
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {userProfile.achievements && userProfile.achievements.length > 0 && (
            <section className="mb-10">
              <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
                Achievements
              </h3>
              <div className="space-y-2">
                {userProfile.achievements.map((achievement, index) => (
                  <div key={index} className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span className="text-slate-700">{achievement}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {userProfile.certifications && userProfile.certifications.length > 0 && (
            <section className="mb-10">
              <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
                Certifications
              </h3>
              <div className="space-y-2">
                {userProfile.certifications.map((cert, index) => (
                  <div key={index} className="flex justify-between">
                    <span className="text-slate-700">{cert}</span>
                    <span className="text-slate-600">2024</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Professional Links
            </h3>
            <div className="space-y-2">
              {userProfile.github && (
                <div className="flex items-center gap-2">
                  <span className="text-slate-600">GitHub:</span>
                  <a href={userProfile.github} className="text-slate-700 underline">{userProfile.github}</a>
                </div>
              )}
              {userProfile.linkedin && (
                <div className="flex items-center gap-2">
                  <span className="text-slate-600">LinkedIn:</span>
                  <a href={userProfile.linkedin} className="text-slate-700 underline">{userProfile.linkedin}</a>
                </div>
              )}
              {userProfile.website && (
                <div className="flex items-center gap-2">
                  <span className="text-slate-600">Website:</span>
                  <a href={userProfile.website} className="text-slate-700 underline">{userProfile.website}</a>
                </div>
              )}
            </div>
          </section>

          {userProfile.profile_completeness && (
            <section className="bg-slate-50 p-6 rounded border">
              <h3 className="text-lg font-bold text-slate-900 mb-2">Profile Completeness</h3>
              <div className="flex items-center gap-4">
                <div className="flex-1 bg-slate-200 rounded-full h-2">
                  <div 
                    className="bg-slate-800 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${userProfile.profile_completeness}%` }}
                  ></div>
                </div>
                <span className="text-slate-700 font-medium">{userProfile.profile_completeness}%</span>
              </div>
            </section>
          )}
        </div>
      </main>
    </div>
  )
}