// import Image from "next/image";

// export default function Home() {
//   return (
//     <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
//       <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
//         <Image
//           className="dark:invert"
//           src="/next.svg"
//           alt="Next.js logo"
//           width={180}
//           height={38}
//           priority
//         />
//         <ol className="font-mono list-inside list-decimal text-sm/6 text-center sm:text-left">
//           <li className="mb-2 tracking-[-.01em]">
//             Get started by editing{" "}
//             <code className="bg-black/[.05] dark:bg-white/[.06] font-mono font-semibold px-1 py-0.5 rounded">
//               app/page.tsx
//             </code>
//             .
//           </li>
//           <li className="tracking-[-.01em]">
//             Save and see your changes instantly.
//           </li>
//         </ol>

//         <div className="flex gap-4 items-center flex-col sm:flex-row">
//           <a
//             className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
//             href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             <Image
//               className="dark:invert"
//               src="/vercel.svg"
//               alt="Vercel logomark"
//               width={20}
//               height={20}
//             />
//             Deploy now
//           </a>
//           <a
//             className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 w-full sm:w-auto md:w-[158px]"
//             href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Read our docs
//           </a>
//         </div>
//       </main>
//       <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
//         <a
//           className="flex items-center gap-2 hover:underline hover:underline-offset-4"
//           href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/file.svg"
//             alt="File icon"
//             width={16}
//             height={16}
//           />
//           Learn
//         </a>
//         <a
//           className="flex items-center gap-2 hover:underline hover:underline-offset-4"
//           href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/window.svg"
//             alt="Window icon"
//             width={16}
//             height={16}
//           />
//           Examples
//         </a>
//         <a
//           className="flex items-center gap-2 hover:underline hover:underline-offset-4"
//           href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/globe.svg"
//             alt="Globe icon"
//             width={16}
//             height={16}
//           />
//           Go to nextjs.org →
//         </a>
//       </footer>
//     </div>
//   );
// }


import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ArrowRight, FileText, Award, Briefcase, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b-4 border-slate-800 shadow-sm">
        <div className="max-w-6xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded bg-slate-800 text-white">
                <FileText className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900" style={{ fontFamily: "Georgia, serif" }}>
                  Professional Carrer Builder
                </h1>
                <p className="text-slate-600">Create Your Digital Career Document</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-8">
        <div className="py-16">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1
                className="text-5xl font-bold text-slate-900 mb-6 leading-tight"
                style={{ fontFamily: "Georgia, serif" }}
              >
                Build Your Professional Career Assistant
              </h1>
              <p className="text-xl text-slate-600 mb-8 leading-relaxed">
                Create a polished, professional resume that showcases your experience, skills, and achievements. Our
                platform helps you build a document that stands out to employers and hiring managers.
              </p>
              <div className="flex gap-4">
                <Link href="/register">
                  <Button size="lg" className="bg-slate-800 hover:bg-slate-900 text-white px-8 py-4 text-lg">
                    Start Creating
                    <ArrowRight className="h-5 w-5 ml-2" />
                  </Button>
                </Link>

              </div>
            </div>

          </div>
        </div>

        {/* <div className="py-16 border-t-2 border-slate-200">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900 mb-4" style={{ fontFamily: "Georgia, serif" }}>
              Professional Resume Features
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Everything you need to create a standout resume that gets you noticed by employers and recruiters.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-8 text-center bg-white border-2 border-slate-200 hover:shadow-lg transition-shadow">
              <div className="p-4 rounded-lg bg-slate-100 w-fit mx-auto mb-6">
                <Award className="h-8 w-8 text-slate-700" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3" style={{ fontFamily: "Georgia, serif" }}>
                Professional Templates
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Choose from expertly designed resume templates that follow industry standards and best practices for
                maximum impact.
              </p>
            </Card>

            <Card className="p-8 text-center bg-white border-2 border-slate-200 hover:shadow-lg transition-shadow">
              <div className="p-4 rounded-lg bg-slate-100 w-fit mx-auto mb-6">
                <Briefcase className="h-8 w-8 text-slate-700" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3" style={{ fontFamily: "Georgia, serif" }}>
                Experience Showcase
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Highlight your professional experience, achievements, and career progression in a clear, compelling
                format.
              </p>
            </Card>

            <Card className="p-8 text-center bg-white border-2 border-slate-200 hover:shadow-lg transition-shadow">
              <div className="p-4 rounded-lg bg-slate-100 w-fit mx-auto mb-6">
                <TrendingUp className="h-8 w-8 text-slate-700" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3" style={{ fontFamily: "Georgia, serif" }}>
                Skills & Growth
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Showcase your technical skills, certifications, and professional development to demonstrate your value.
              </p>
            </Card>
          </div>
        </div> */}

        {/* <div className="py-16 text-center">
          <Card className="p-12 bg-slate-800 text-white">
            <h2 className="text-3xl font-bold mb-4" style={{ fontFamily: "Georgia, serif" }}>
              Ready to Build Your Professional Resume?
            </h2>
            <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
              Join thousands of professionals who have created standout resumes that land interviews and advance
              careers.
            </p>
            <Link href="/register">
              <Button
                size="lg"
                variant="secondary"
                className="bg-white text-slate-800 hover:bg-slate-100 px-8 py-4 text-lg"
              >
                Create Your Resume Now
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
            </Link>
          </Card>
        </div> */}
      </div>
    </div>
  )
}
