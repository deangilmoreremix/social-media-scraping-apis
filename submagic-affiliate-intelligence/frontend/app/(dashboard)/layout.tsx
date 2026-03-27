import Link from "next/link";
import { 
  Users, 
  BarChart3, 
  FileText, 
  Sparkles,
  ArrowRight,
  Search,
  Upload
} from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="font-bold text-xl text-slate-900">Submagic AI</span>
            </Link>
          </div>
          <nav className="hidden md:flex items-center gap-2">
            <Link 
              href="/creators" 
              className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-slate-100 transition-colors text-slate-700"
            >
              <Users className="w-4 h-4" />
              Creators
            </Link>
            <Link 
              href="/reports" 
              className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-slate-100 transition-colors text-slate-700"
            >
              <BarChart3 className="w-4 h-4" />
              Reports
            </Link>
            <Link 
              href="/materials" 
              className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-slate-100 transition-colors text-slate-700"
            >
              <FileText className="w-4 h-4" />
              Materials
            </Link>
          </nav>
          <Link 
            href="/creators" 
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2 text-sm"
          >
            <Search className="w-4 h-4" />
            Analyze Creator
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
}
