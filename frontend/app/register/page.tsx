
"use client"
import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { ArrowRight, ArrowLeft, FileText, CheckCircle, Plus, X } from "lucide-react"
import { error } from "console"
import { useRouter } from "next/router"

const skillOptions = [
  "React", "TypeScript", "Next.js", "Node.js", "Python", "JavaScript", "Vue.js", "Angular",
  "GraphQL", "AWS", "Docker", "Kubernetes", "Tailwind CSS", "MongoDB", "PostgreSQL", "Redis",
  "Git", "CI/CD", "Machine Learning", "Data Science", "DevOps", "Microservices"
]

const certificationOptions = [
  "AWS Certified Solutions Architect", "Google Cloud Professional", "Microsoft Azure Fundamentals",
  "Certified Kubernetes Administrator", "PMP", "Scrum Master", "CompTIA Security+", "CISSP"
]

const trendingSkills = [
  "AI/ML", "Blockchain", "Cloud Computing", "Cybersecurity", "Data Analytics",
  "IoT", "Serverless", "Edge Computing", "Quantum Computing", "Web3"
]

type FormDataType = {
  email: string
  name: string
  age: string
  location: string
  github: string
  linkedin: string
  huggingface: string
  x: string
  website: string
  currentRole: string
  company: string
  experienceLevel: string
  bio: string
  skills: string[]
  certifications: string[]
  projects: { id: number; title: string; description: string; technologies: string; link: string }[]
  blogs: { id: number; title: string; url: string; description: string }[]
  achievements: string[]
  careerGoals: string[]
  timeframe: string
  priorities: string
  trending_skills: string[]
  skill_gap_analysis: Record<string, any>
  recommendations: any[]
  network_opportunities: any[]
}

export default function ComprehensiveRegisterPage() {
// const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<FormDataType>({
    email: "",
    name: "",
    age: "",
    location: "",
    github: "",
    linkedin: "",
    huggingface: "",
    x: "",
    website: "",
    currentRole: "",
    company: "",
    experienceLevel: "",
    bio: "",
    skills: [],
    certifications: [],
    projects: [],
    blogs: [],
    achievements: [],
    careerGoals: [],
    timeframe: "",
    priorities: "",
    trending_skills: [],
    skill_gap_analysis: {},
    recommendations: [],
    network_opportunities: []
  })

  // Project and Blog management
  const [newProject, setNewProject] = useState({ title: "", description: "", technologies: "", link: "" })
  const [newBlog, setNewBlog] = useState({ title: "", url: "", description: "" })
  const [newAchievement, setNewAchievement] = useState("")

  const totalSteps = 6
  const progress = (currentStep / totalSteps) * 100

  const handleSkillToggle = (skill :string) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.includes(skill) 
        ? prev.skills.filter(s => s !== skill) 
        : [...prev.skills, skill]
    }))
  }

  const handleCertificationToggle = (cert :string) => {
    setFormData(prev => ({
      ...prev,
      certifications: prev.certifications.includes(cert)
        ? prev.certifications.filter(c => c !== cert)
        : [...prev.certifications, cert]
    }))
  }

  const addProject = () => {
    if (newProject.title && newProject.description) {
      setFormData(prev => ({
        ...prev,
        projects: [...prev.projects, { ...newProject, id: Date.now() }]
      }))
      setNewProject({ title: "", description: "", technologies: "", link: "" })
    }
  }

  const removeProject = (id : number) => {
    setFormData(prev => ({
      ...prev,
      projects: prev.projects.filter(p => p.id !== id)
    }))
  }

  const addBlog = () => {
    if (newBlog.title && newBlog.url) {
      setFormData(prev => ({
        ...prev,
        blogs: [...prev.blogs, { ...newBlog, id: Date.now() }]
      }))
      setNewBlog({ title: "", url: "", description: "" })
    }
  }

  const removeBlog = (id:number) => {
    setFormData(prev => ({
      ...prev,
      blogs: prev.blogs.filter(b => b.id !== id)
    }))
  }

  const addAchievement = () => {
    if (newAchievement.trim()) {
      setFormData(prev => ({
        ...prev,
        achievements: [...prev.achievements, newAchievement.trim()]
      }))
      setNewAchievement("")
    }
  }

  const removeAchievement = (index:number) => {
    setFormData(prev => ({
      ...prev,
      achievements: prev.achievements.filter((_, i) => i !== index)
    }))
  }

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }



const handleSubmit = async () => {
  try {
    // Prepare the data according to your UserProfile schema
    const profileData = {
      email: formData.email,
      name: formData.name,
      age: formData.age ? parseInt(formData.age) : null,
      location: formData.location || null,
      github: formData.github || null,
      linkedin: formData.linkedin || null,
      huggingface: formData.huggingface || null,
      x: formData.x || null,
      website: formData.website || null,
      certifications: formData.certifications && formData.certifications.length > 0 ? formData.certifications : null,
      skills: formData.skills && formData.skills.length > 0 ? formData.skills : null,
      projects: formData.projects || [],
      blogs: formData.blogs && formData.blogs.length > 0 ? formData.blogs : null,
      achievements: formData.achievements && formData.achievements.length > 0 ? formData.achievements : null,
      bio: formData.bio || null,
      trending_skills: null,
      skill_gap_analysis: null,
      recommendations: null,
      network_opportunities: null
    };

    console.log("Profile data to submit:", profileData);

    // Make the API call
    const response = await fetch("http://127.0.0.1:8000/registration", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify(profileData)
    });

    console.log("Response status:", response.status);
    console.log("Response headers:", response.headers);

    // Check if the response is ok
    if (!response.ok) {
      const errorText = await response.text();
      console.error("HTTP Error:", response.status, errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    // Parse the JSON response
    const responseData = await response.json();
    console.log("Registration successful:", responseData);

    // Store user data for dashboard (optional)
    localStorage.setItem("userProfile", JSON.stringify({
      ...profileData,
      user_id: responseData.user_id,
      profile_completeness: responseData.profile_completeness
    }));

    // Show success message
    alert(`Registration successful! Welcome ${responseData.user_name}!`);

    // Navigate to dashboard
    // router.push("/dashboard");
    window.location.href="/dashboard"

  } catch (error:any) {
    console.error("Registration failed:", error);
    
    // Show user-friendly error message
    if (error.message.includes("Failed to fetch")) {
      alert("Cannot connect to server. Please make sure the backend is running on http://127.0.0.1:8000");
    } else if (error.message.includes("422")) {
      alert("Please check your form data. Some fields may be invalid.");
    } else {
      alert(`Registration failed: ${error.message}`);
    }
  }
};

  const isStepValid = () => {
    switch (currentStep) {
      case 1: return formData.name && formData.email
      case 2: return formData.github || formData.linkedin || formData.website
      case 3: return formData.skills.length > 0
      case 4: return true // Projects are optional
      case 5: return true // Blogs are optional
      case 6: return true // Goals are optional
      default: return false
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 rounded-lg bg-slate-800 text-white">
              <FileText className="h-6 w-6" />
            </div>
            <h1 className="text-4xl font-bold text-slate-900">Build Your Professional Profile</h1>
          </div>
          <p className="text-slate-600 text-lg">Create a comprehensive profile for career growth</p>
        </div>

        <div className="mb-8 bg-white rounded-lg p-4 shadow-sm border">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
              Step {currentStep} of {totalSteps}
            </span>
            <span className="text-sm text-slate-500">{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-3" />
        </div>

        <Card className="p-12 bg-white shadow-lg border-2 border-slate-200">
          {/* Step 1: Basic Information */}
          {currentStep === 1 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Basic Information</h2>
                <p className="text-slate-600 mt-1">Essential personal details</p>
              </div>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="name" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Full Name *
                  </Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="John Smith"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Email Address *
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="john.smith@email.com"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="age" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Age
                  </Label>
                  <Input
                    id="age"
                    type="number"
                    min="0"
                    value={formData.age}
                    onChange={(e) => setFormData(prev => ({ ...prev, age: e.target.value }))}
                    placeholder="28"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="location" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Location
                  </Label>
                  <Input
                    id="location"
                    value={formData.location}
                    onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                    placeholder="San Francisco, CA"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Social Links */}
          {currentStep === 2 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Social Links</h2>
                <p className="text-slate-600 mt-1">Connect your professional profiles</p>
              </div>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="github" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    GitHub Profile
                  </Label>
                  <Input
                    id="github"
                    value={formData.github}
                    onChange={(e) => setFormData(prev => ({ ...prev, github: e.target.value }))}
                    placeholder="https://github.com/username"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="linkedin" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    LinkedIn Profile
                  </Label>
                  <Input
                    id="linkedin"
                    value={formData.linkedin}
                    onChange={(e) => setFormData(prev => ({ ...prev, linkedin: e.target.value }))}
                    placeholder="https://linkedin.com/in/username"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="huggingface" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    HuggingFace Profile
                  </Label>
                  <Input
                    id="huggingface"
                    value={formData.huggingface}
                    onChange={(e) => setFormData(prev => ({ ...prev, huggingface: e.target.value }))}
                    placeholder="https://huggingface.co/username"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="x" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    X (Twitter) Profile
                  </Label>
                  <Input
                    id="x"
                    value={formData.x}
                    onChange={(e) => setFormData(prev => ({ ...prev, x: e.target.value }))}
                    placeholder="https://x.com/username"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
                
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="website" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Personal Website
                  </Label>
                  <Input
                    id="website"
                    value={formData.website}
                    onChange={(e) => setFormData(prev => ({ ...prev, website: e.target.value }))}
                    placeholder="https://yourwebsite.com"
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Skills & Certifications */}
          {currentStep === 3 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Skills & Certifications</h2>
                <p className="text-slate-600 mt-1">Your technical expertise and credentials</p>
              </div>
              
              <div className="space-y-8">
                {/* Skills Section */}
                <div>
                  <Label className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4 block">
                    Technical Skills *
                  </Label>
                  <div className="grid grid-cols-4 gap-3">
                    {skillOptions.map(skill => (
                      <div key={skill} className="flex items-center space-x-2 p-2 rounded border border-slate-200 hover:bg-slate-50">
                        <Checkbox
                          id={skill}
                          checked={formData.skills.includes(skill)}
                          onCheckedChange={() => handleSkillToggle(skill)}
                        />
                        <Label htmlFor={skill} className="text-sm font-medium text-slate-700">{skill}</Label>
                      </div>
                    ))}
                  </div>
                  {formData.skills.length > 0 && (
                    <div className="mt-4 p-4 bg-slate-50 rounded border">
                      <div className="flex flex-wrap gap-2">
                        {formData.skills.map(skill => (
                          <Badge key={skill} variant="secondary" className="bg-slate-800 text-white">{skill}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Certifications Section */}
                <div>
                  <Label className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4 block">
                    Certifications
                  </Label>
                  <div className="grid grid-cols-2 gap-3">
                    {certificationOptions.map(cert => (
                      <div key={cert} className="flex items-center space-x-2 p-2 rounded border border-slate-200 hover:bg-slate-50">
                        <Checkbox
                          id={cert}
                          checked={formData.certifications.includes(cert)}
                          onCheckedChange={() => handleCertificationToggle(cert)}
                        />
                        <Label htmlFor={cert} className="text-sm font-medium text-slate-700">{cert}</Label>
                      </div>
                    ))}
                  </div>
                  {formData.certifications.length > 0 && (
                    <div className="mt-4 p-4 bg-slate-50 rounded border">
                      <div className="flex flex-wrap gap-2">
                        {formData.certifications.map(cert => (
                          <Badge key={cert} variant="outline" className="border-slate-800 text-slate-800">{cert}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Projects */}
          {currentStep === 4 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Projects</h2>
                <p className="text-slate-600 mt-1">Showcase your work and achievements</p>
              </div>
              
              <div className="space-y-6">
                {/* Add New Project */}
                <div className="p-6 border border-slate-200 rounded-lg bg-slate-50">
                  <h3 className="text-lg font-semibold text-slate-800 mb-4">Add New Project</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      placeholder="Project Title"
                      value={newProject.title}
                      onChange={(e) => setNewProject(prev => ({ ...prev, title: e.target.value }))}
                      className="border-slate-300"
                    />
                    <Input
                      placeholder="Project Link (optional)"
                      value={newProject.link}
                      onChange={(e) => setNewProject(prev => ({ ...prev, link: e.target.value }))}
                      className="border-slate-300"
                    />
                    <div className="col-span-2">
                      <Textarea
                        placeholder="Project Description"
                        value={newProject.description}
                        onChange={(e) => setNewProject(prev => ({ ...prev, description: e.target.value }))}
                        className="border-slate-300"
                        rows={3}
                      />
                    </div>
                    <Input
                      placeholder="Technologies Used (comma-separated)"
                      value={newProject.technologies}
                      onChange={(e) => setNewProject(prev => ({ ...prev, technologies: e.target.value }))}
                      className="border-slate-300"
                    />
                    <div className="flex items-end">
                      <Button onClick={addProject} className="bg-slate-800 hover:bg-slate-900 text-white">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Project
                      </Button>
                    </div>
                  </div>
                </div>

                {/* Existing Projects */}
                {formData.projects.length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-slate-800">Your Projects</h3>
                    {formData.projects.map(project => (
                      <div key={project.id} className="p-4 border border-slate-200 rounded-lg bg-white">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h4 className="font-semibold text-slate-800">{project.title}</h4>
                            <p className="text-slate-600 mt-1">{project.description}</p>
                            {project.technologies && (
                              <p className="text-sm text-slate-500 mt-2">Technologies: {project.technologies}</p>
                            )}
                            {project.link && (
                              <a href={project.link} className="text-slate-800 text-sm underline mt-2 inline-block">
                                View Project
                              </a>
                            )}
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => removeProject(project.id)}
                            className="text-red-600 border-red-600 hover:bg-red-50"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Step 5: Blogs & Achievements */}
          {currentStep === 5 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Blogs & Achievements</h2>
                <p className="text-slate-600 mt-1">Share your writing and accomplishments</p>
              </div>
              
              <div className="space-y-8">
                {/* Blogs Section */}
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-4">Blog Articles</h3>
                  <div className="p-6 border border-slate-200 rounded-lg bg-slate-50 mb-4">
                    <div className="grid grid-cols-2 gap-4">
                      <Input
                        placeholder="Blog Title"
                        value={newBlog.title}
                        onChange={(e) => setNewBlog(prev => ({ ...prev, title: e.target.value }))}
                        className="border-slate-300"
                      />
                      <Input
                        placeholder="Blog URL"
                        value={newBlog.url}
                        onChange={(e) => setNewBlog(prev => ({ ...prev, url: e.target.value }))}
                        className="border-slate-300"
                      />
                      <div className="col-span-2">
                        <Textarea
                          placeholder="Brief Description"
                          value={newBlog.description}
                          onChange={(e) => setNewBlog(prev => ({ ...prev, description: e.target.value }))}
                          className="border-slate-300"
                          rows={2}
                        />
                      </div>
                      <div className="col-span-2">
                        <Button onClick={addBlog} className="bg-slate-800 hover:bg-slate-900 text-white">
                          <Plus className="h-4 w-4 mr-2" />
                          Add Blog
                        </Button>
                      </div>
                    </div>
                  </div>

                  {formData.blogs.length > 0 && (
                    <div className="space-y-3">
                      {formData.blogs.map(blog => (
                        <div key={blog.id} className="p-4 border border-slate-200 rounded-lg bg-white">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-semibold text-slate-800">{blog.title}</h4>
                              {blog.description && <p className="text-slate-600 text-sm mt-1">{blog.description}</p>}
                              <a href={blog.url} className="text-slate-800 text-sm underline mt-2 inline-block">
                                Read Article
                              </a>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => removeBlog(blog.id)}
                              className="text-red-600 border-red-600 hover:bg-red-50"
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Achievements Section */}
                <div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-4">Achievements</h3>
                  <div className="p-6 border border-slate-200 rounded-lg bg-slate-50 mb-4">
                    <div className="flex gap-4">
                      <Input
                        placeholder="Describe an achievement..."
                        value={newAchievement}
                        onChange={(e) => setNewAchievement(e.target.value)}
                        className="border-slate-300 flex-1"
                      />
                      <Button onClick={addAchievement} className="bg-slate-800 hover:bg-slate-900 text-white">
                        <Plus className="h-4 w-4 mr-2" />
                        Add
                      </Button>
                    </div>
                  </div>

                  {formData.achievements.length > 0 && (
                    <div className="space-y-2">
                      {formData.achievements.map((achievement, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border border-slate-200 rounded-lg bg-white">
                          <span className="text-slate-800">{achievement}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => removeAchievement(index)}
                            className="text-red-600 border-red-600 hover:bg-red-50"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Step 6: Career Goals & Summary */}
          {currentStep === 6 && (
            <div className="space-y-8">
              <div className="border-b-2 border-slate-800 pb-4 mb-8">
                <h2 className="text-2xl font-bold text-slate-900 uppercase tracking-wide">Career Goals & Summary</h2>
                <p className="text-slate-600 mt-1">Define your professional aspirations</p>
              </div>
              
              <div className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="bio" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Professional Summary
                  </Label>
                  <Textarea
                    id="bio"
                    value={formData.bio}
                    onChange={(e) => setFormData(prev => ({ ...prev, bio: e.target.value }))}
                    placeholder="Write a compelling professional summary that highlights your expertise, experience, and career objectives..."
                    rows={4}
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="priorities" className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                    Career Goals & Priorities
                  </Label>
                  <Textarea
                    id="priorities"
                    value={formData.priorities}
                    onChange={(e) => setFormData(prev => ({ ...prev, priorities: e.target.value }))}
                    placeholder="Describe your career goals, preferred industries, target roles, and what you're looking to achieve..."
                    rows={4}
                    className="border-slate-300 focus:border-slate-800"
                  />
                </div>

                <div className="p-6 bg-slate-50 border border-slate-200 rounded-lg">
                  <h3 className="text-lg font-semibold text-slate-800 mb-4">AI-Powered Insights</h3>
                  <p className="text-slate-600 text-sm">
                    After registration, our AI will analyze your profile to provide:
                  </p>
                  <ul className="mt-3 space-y-2 text-sm text-slate-600">
                    <li>• Trending skills in your field</li>
                    <li>• Skill gap analysis and recommendations</li>
                    <li>• Personalized career suggestions</li>
                    <li>• Network opportunities and connections</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          <div className="flex justify-between mt-12 pt-8 border-t-2 border-slate-200">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className="border-slate-300 text-slate-700 hover:bg-slate-50 bg-transparent"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Previous Step
            </Button>
            
            {currentStep < totalSteps ? (
              <Button
                onClick={handleNext}
                disabled={!isStepValid()}
                className="bg-slate-800 hover:bg-slate-900 text-white"
              >
                Next Step
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                disabled={!isStepValid()}
                className="bg-slate-800 hover:bg-slate-900 text-white"
              >
                Complete Registration
                <CheckCircle className="h-4 w-4 ml-2" />
              </Button>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}