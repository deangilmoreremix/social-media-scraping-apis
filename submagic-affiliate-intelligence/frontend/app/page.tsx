import Link from "next/link";
import { 
  Users, 
  BarChart3, 
  FileText, 
  Zap, 
  ArrowRight,
  Sparkles,
  Target,
  TrendingUp
} from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-xl">Submagic AI</span>
          </div>
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/creators" className="text-slate-600 hover:text-indigo-600 transition-colors">
              Creators
            </Link>
            <Link href="/reports" className="text-slate-600 hover:text-indigo-600 transition-colors">
              Reports
            </Link>
            <Link href="/materials" className="text-slate-600 hover:text-indigo-600 transition-colors">
              Materials
            </Link>
          </nav>
          <Link 
            href="/creators" 
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2"
          >
            Get Started <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      <main>
        <section className="py-24 px-4">
          <div className="container mx-auto text-center max-w-4xl">
            <div className="inline-flex items-center gap-2 bg-indigo-100 text-indigo-700 px-4 py-2 rounded-full text-sm font-medium mb-8">
              <Zap className="w-4 h-4" />
              Powered by GPT-4o Analysis
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight">
              Find the Perfect
              <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"> Affiliate Materials</span>
              <br />for Every Creator
            </h1>
            <p className="text-xl text-slate-600 mb-12 max-w-2xl mx-auto">
              Our AI analyzes creator profiles and recommends the most effective Submagic affiliate 
              content based on their audience, content style, and engagement patterns.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/creators" 
                className="bg-indigo-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2 text-lg"
              >
                <Users className="w-5 h-5" />
                Analyze a Creator
              </Link>
              <Link 
                href="/reports" 
                className="bg-white text-slate-700 px-8 py-4 rounded-xl font-semibold hover:bg-slate-50 transition-colors border border-slate-200 flex items-center justify-center gap-2 text-lg"
              >
                <FileText className="w-5 h-5" />
                View Reports
              </Link>
            </div>
          </div>
        </section>

        <section className="py-24 px-4 bg-white">
          <div className="container mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-indigo-50 to-indigo-100/50 border border-indigo-100">
                <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Users className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">1. Analyze Profile</h3>
                <p className="text-slate-600">
                  Input any social media profile URL. We scrape and analyze their audience, 
                  content themes, and engagement patterns.
                </p>
              </div>
              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-purple-100/50 border border-purple-100">
                <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Target className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">2. AI Matching</h3>
                <p className="text-slate-600">
                  Our GPT-4o powered engine matches the creator with our library of 
                  affiliate materials to find the perfect fit.
                </p>
              </div>
              <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-pink-50 to-pink-100/50 border border-pink-100">
                <div className="w-16 h-16 bg-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">3. Get Results</h3>
                <p className="text-slate-600">
                  Receive detailed reports with recommendations, score cards, 
                  and specific tips for maximum conversion.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24 px-4">
          <div className="container mx-auto max-w-5xl">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">Affiliate Materials Library</h2>
            <p className="text-slate-600 text-center mb-12 max-w-2xl mx-auto">
              Pre-built templates and resources optimized for different platforms and content types
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { name: "YouTube Reviews", type: "Long Form", icon: "🎥", desc: "In-depth review scripts for 5-10 minute videos" },
                { name: "TikTok Demos", type: "Short Form", icon: "📱", desc: "15-30 second hooks showcasing key features" },
                { name: "Instagram Reels", type: "Tutorial", icon: "✨", desc: "Step-by-step tutorials with clear CTAs" },
                { name: "Email Templates", type: "Outreach", icon: "📧", desc: "Professional templates for affiliate outreach" },
                { name: "Comparison Posts", type: "Review", icon: "⚖️", desc: "vs competitors - honest pros and cons" },
                { name: "Success Stories", type: "Testimonial", icon: "📖", desc: "Share your personal transformation story" },
              ].map((material, i) => (
                <div key={i} className="bg-white p-6 rounded-xl border border-slate-200 hover:border-indigo-200 hover:shadow-lg transition-all">
                  <div className="text-4xl mb-4">{material.icon}</div>
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-semibold text-slate-900">{material.name}</h3>
                    <span className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-full">{material.type}</span>
                  </div>
                  <p className="text-slate-600 text-sm">{material.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-24 px-4 bg-gradient-to-br from-indigo-600 to-purple-700 text-white">
          <div className="container mx-auto text-center max-w-3xl">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Boost Affiliate Conversions?</h2>
            <p className="text-indigo-100 text-lg mb-8">
              Start analyzing creators and get AI-powered recommendations in seconds
            </p>
            <Link 
              href="/creators" 
              className="bg-white text-indigo-600 px-8 py-4 rounded-xl font-semibold hover:bg-indigo-50 transition-colors inline-flex items-center gap-2 text-lg"
            >
              <BarChart3 className="w-5 h-5" />
              Start Analyzing Now
            </Link>
          </div>
        </section>
      </main>

      <footer className="bg-slate-900 text-slate-400 py-12 px-4">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="font-semibold text-white">Submagic Affiliate Intelligence</span>
            </div>
            <div className="flex gap-6 text-sm">
              <Link href="/creators" className="hover:text-white transition-colors">Creators</Link>
              <Link href="/reports" className="hover:text-white transition-colors">Reports</Link>
              <Link href="/materials" className="hover:text-white transition-colors">Materials</Link>
            </div>
            <p className="text-sm">© 2026 Submagic. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
