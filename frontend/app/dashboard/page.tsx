"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { LogOut, FileText, MapPin, Mail, Phone, Download, Edit, Printer } from "lucide-react"

interface UserProfile {
  firstName: string
  lastName: string
  email: string
  currentRole: string
  company: string
  experienceLevel: string
  skills: string[]
  bio: string
  careerGoals: string[]
  timeframe: string
  priorities: string
}

export default function DashboardPage() {
  const router = useRouter()
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    // Check if user has completed registration
    const storedProfile = localStorage.getItem("userProfile")
    if (!storedProfile) {
      router.push("/register")
      return
    }

    setUserProfile(JSON.parse(storedProfile))
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem("userProfile")
    router.push("/")
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
              {userProfile.firstName} {userProfile.lastName}
            </h1>
            <h2 className="text-2xl text-slate-700 font-normal mb-6 italic">{userProfile.currentRole}</h2>
            <div className="flex flex-wrap justify-center gap-8 text-slate-600">
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                <span>{userProfile.email}</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                <span>San Francisco, CA</span>
              </div>
            </div>
          </header>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-4 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Professional Summary
            </h3>
            <p className="text-slate-700 leading-relaxed text-lg">
              {userProfile.bio ||
                `Accomplished ${userProfile.currentRole} with ${userProfile.experienceLevel.toLowerCase()} of progressive experience in technology solutions. Demonstrated expertise in modern development practices, team leadership, and delivering scalable applications that drive business growth. Passionate about innovation and committed to excellence in every project.`}
            </p>
          </section>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-4 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Core Competencies
            </h3>
            <div className="grid grid-cols-4 gap-4">
              {userProfile.skills.map((skill, index) => (
                <div key={skill} className="text-slate-700 font-medium">
                  • {skill}
                </div>
              ))}
            </div>
          </section>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Professional Experience
            </h3>
            <div className="space-y-8">
              <div>
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-slate-900">{userProfile.currentRole}</h4>
                    <p className="text-lg text-slate-700 font-medium italic">
                      {userProfile.company || "Current Company"}
                    </p>
                  </div>
                  <div className="text-right text-slate-600">
                    <div className="font-medium">January 2022 - Present</div>
                    <div className="text-sm">San Francisco, CA</div>
                  </div>
                </div>
                <ul className="space-y-2 text-slate-700 ml-6">
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Spearheaded development of enterprise-scale web applications serving over 100,000 active users,
                      utilizing modern frameworks and cloud infrastructure
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Led cross-functional teams of 8+ developers, designers, and product managers to deliver complex
                      projects 20% ahead of schedule
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Implemented comprehensive testing strategies and CI/CD pipelines, reducing production bugs by 40%
                      and deployment time by 60%
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Mentored 5+ junior developers through code reviews, technical guidance, and career development
                      planning
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Architected microservices infrastructure supporting 99.9% uptime and handling 10M+ API requests
                      daily
                    </span>
                  </li>
                </ul>
              </div>

              <div>
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-slate-900">Senior Software Developer</h4>
                    <p className="text-lg text-slate-700 font-medium italic">Tech Innovations Inc.</p>
                  </div>
                  <div className="text-right text-slate-600">
                    <div className="font-medium">March 2020 - December 2021</div>
                    <div className="text-sm">Remote</div>
                  </div>
                </div>
                <ul className="space-y-2 text-slate-700 ml-6">
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Developed and maintained 12+ client-facing applications using React, Node.js, and cloud services
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Optimized database queries and application performance, achieving 60% improvement in load times
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Collaborated in agile development environment, participating in sprint planning, code reviews, and
                      technical discussions
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Contributed to open-source projects and maintained comprehensive technical documentation
                    </span>
                  </li>
                </ul>
              </div>

              <div>
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-slate-900">Software Developer</h4>
                    <p className="text-lg text-slate-700 font-medium italic">StartupCorp</p>
                  </div>
                  <div className="text-right text-slate-600">
                    <div className="font-medium">June 2018 - February 2020</div>
                    <div className="text-sm">San Francisco, CA</div>
                  </div>
                </div>
                <ul className="space-y-2 text-slate-700 ml-6">
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>
                      Built responsive web applications from concept to deployment using modern JavaScript frameworks
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>Integrated third-party APIs and payment systems, increasing user engagement by 35%</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-slate-400 mr-3 mt-2">•</span>
                    <span>Participated in product planning and user experience design decisions</span>
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Education
            </h3>
            <div className="flex justify-between items-start">
              <div>
                <h4 className="text-lg font-bold text-slate-900">Bachelor of Science in Computer Science</h4>
                <p className="text-lg text-slate-700 font-medium italic">University of California, Berkeley</p>
                <p className="text-slate-600 mt-1">Magna Cum Laude • GPA: 3.8/4.0</p>
                <p className="text-slate-600">
                  Relevant Coursework: Data Structures, Algorithms, Software Engineering, Database Systems
                </p>
              </div>
              <div className="text-right text-slate-600">
                <div className="font-medium">May 2018</div>
                <div className="text-sm">Berkeley, CA</div>
              </div>
            </div>
          </section>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Key Projects
            </h3>
            <div className="space-y-6">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-lg font-bold text-slate-900">E-Commerce Platform Redesign</h4>
                  <span className="text-slate-600 font-medium">2023</span>
                </div>
                <p className="text-slate-600 text-sm mb-2 italic">React, Node.js, PostgreSQL, AWS</p>
                <p className="text-slate-700">
                  Led complete architectural redesign of legacy e-commerce platform, implementing modern microservices
                  architecture. Resulted in 35% increase in conversion rates, 50% improvement in page load times, and
                  enhanced user experience across mobile and desktop platforms.
                </p>
              </div>
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-lg font-bold text-slate-900">Real-time Analytics Dashboard</h4>
                  <span className="text-slate-600 font-medium">2022</span>
                </div>
                <p className="text-slate-600 text-sm mb-2 italic">Vue.js, Python, Redis, Docker</p>
                <p className="text-slate-700">
                  Architected and developed real-time analytics dashboard processing over 1 million events daily.
                  Implemented efficient data visualization with sub-second response times and customizable reporting
                  features for executive decision-making.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-10">
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Certifications & Awards
            </h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h4 className="font-bold text-slate-900 mb-3">Professional Certifications</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-700">AWS Certified Solutions Architect - Professional</span>
                    <span className="text-slate-600">2023</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-700">Google Cloud Professional Developer</span>
                    <span className="text-slate-600">2022</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-700">Certified Kubernetes Administrator (CKA)</span>
                    <span className="text-slate-600">2022</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-bold text-slate-900 mb-3">Recognition & Awards</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-700">Employee of the Year</span>
                    <span className="text-slate-600">2023</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-700">Innovation Award - Best Technical Solution</span>
                    <span className="text-slate-600">2022</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-700">Dean's List - UC Berkeley</span>
                    <span className="text-slate-600">2016-2018</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-xl font-bold text-slate-900 mb-6 uppercase tracking-wider border-b-2 border-slate-300 pb-2">
              Professional Affiliations
            </h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <div className="space-y-2 text-slate-700">
                  <div>• Association for Computing Machinery (ACM)</div>
                  <div>• IEEE Computer Society</div>
                  <div>• Women in Technology International</div>
                </div>
              </div>
              <div>
                <div className="space-y-2 text-slate-700">
                  <div>• San Francisco Tech Meetup - Organizer</div>
                  <div>• Open Source Contributor - GitHub</div>
                  <div>• Tech Conference Speaker (5+ events)</div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
