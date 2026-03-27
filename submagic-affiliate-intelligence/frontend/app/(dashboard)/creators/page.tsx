"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { 
  Search, 
  Upload, 
  Instagram, 
  Youtube, 
  Twitter,
  Loader2,
  CheckCircle2,
  AlertCircle,
  FileText,
  TrendingUp
} from "lucide-react";

const PLATFORM_ICONS: Record<string, React.ReactNode> = {
  instagram: <Instagram className="w-5 h-5 text-pink-500" />,
  youtube: <Youtube className="w-5 h-5 text-red-500" />,
  tiktok: <span className="text-lg">🎵</span>,
  twitter: <Twitter className="w-5 h-5 text-blue-400" />,
};

export default function CreatorsPage() {
  const [profileUrl, setProfileUrl] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "text/csv": [".csv"],
    },
    onDrop: async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (file) {
        await handleBulkUpload(file);
      }
    },
  });

  const handleAnalyze = async () => {
    if (!profileUrl.trim()) return;
    
    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/creators/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profile_url: profileUrl }),
      });

      if (!response.ok) throw new Error("Analysis failed");
      
      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setError("Failed to analyze profile. Please try again.");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleBulkUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/creators/bulk-analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Bulk analysis failed");
      
      const data = await response.json();
      setAnalysisResult({ bulk: true, ...data });
    } catch (err) {
      setError("Failed to process file. Please try again.");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Creator Analysis</h1>
        <p className="text-slate-600">
          Analyze any social media profile to get AI-powered affiliate material recommendations
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-indigo-600" />
            Single Profile Analysis
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Social Media Profile URL
              </label>
              <input
                type="url"
                value={profileUrl}
                onChange={(e) => setProfileUrl(e.target.value)}
                placeholder="https://instagram.com/username or https://tiktok.com/@username"
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all"
              />
            </div>
            
            <button
              onClick={handleAnalyze}
              disabled={!profileUrl.trim() || isAnalyzing}
              className="w-full bg-indigo-600 text-white py-3 rounded-xl font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Analyze Profile
                </>
              )}
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-slate-100">
            <p className="text-sm text-slate-500 mb-3">Supported platforms:</p>
            <div className="flex gap-3">
              <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg">
                <Instagram className="w-4 h-4 text-pink-500" />
                <span className="text-sm">Instagram</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg">
                <span className="text-lg">🎵</span>
                <span className="text-sm">TikTok</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg">
                <Youtube className="w-4 h-4 text-red-500" />
                <span className="text-sm">YouTube</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-lg">
                <Twitter className="w-4 h-4 text-blue-400" />
                <span className="text-sm">Twitter/X</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Upload className="w-5 h-5 text-indigo-600" />
            Bulk CSV Upload
          </h2>
          
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
              isDragActive 
                ? "border-indigo-500 bg-indigo-50" 
                : "border-slate-200 hover:border-indigo-300"
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <p className="text-slate-600 mb-2">
              {isDragActive ? "Drop the CSV file here" : "Drag & drop a CSV file here"}
            </p>
            <p className="text-sm text-slate-400">
              or click to select. File should contain a &quot;url&quot; or &quot;profile_url&quot; column.
            </p>
          </div>

          <div className="mt-4 p-4 bg-slate-50 rounded-lg">
            <p className="text-sm font-medium text-slate-700 mb-2">CSV Format Example:</p>
            <code className="text-xs text-slate-600">
              url{`\n`}
              https://instagram.com/creator1{`\n`}
              https://tiktok.com/@creator2{`\n`}
              https://youtube.com/@creator3
            </code>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-8 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {analysisResult && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-6">
            <CheckCircle2 className="w-6 h-6 text-green-500" />
            <h2 className="text-xl font-semibold">Analysis Complete</h2>
          </div>

          {analysisResult.bulk ? (
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-indigo-50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-indigo-600">{analysisResult.total}</div>
                  <div className="text-sm text-slate-600">Total Analyzed</div>
                </div>
                <div className="bg-green-50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-green-600">{analysisResult.success?.length || 0}</div>
                  <div className="text-sm text-slate-600">Successful</div>
                </div>
                <div className="bg-red-50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-red-600">{analysisResult.failed?.length || 0}</div>
                  <div className="text-sm text-slate-600">Failed</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="flex items-center gap-4 pb-6 border-b border-slate-100">
                {PLATFORM_ICONS[analysisResult.creator?.platform] || <div className="w-12 h-12 bg-slate-200 rounded-full" />}
                <div>
                  <h3 className="text-xl font-semibold">@{analysisResult.creator?.username || "Unknown"}</h3>
                  <p className="text-slate-500 capitalize">{analysisResult.creator?.platform}</p>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-4">
                <div className="bg-slate-50 rounded-xl p-4">
                  <div className="text-2xl font-bold text-slate-900">
                    {analysisResult.creator?.follower_count?.toLocaleString() || "N/A"}
                  </div>
                  <div className="text-sm text-slate-500">Followers</div>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <div className="text-2xl font-bold text-slate-900">
                    {analysisResult.creator?.engagement_rate || "N/A"}%
                  </div>
                  <div className="text-sm text-slate-500">Engagement</div>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <div className="text-2xl font-bold text-slate-900">
                    {analysisResult.creator?.total_posts || "N/A"}
                  </div>
                  <div className="text-sm text-slate-500">Total Posts</div>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <div className="text-2xl font-bold text-slate-900">
                    {analysisResult.creator?.is_verified ? "Yes" : "No"}
                  </div>
                  <div className="text-sm text-slate-500">Verified</div>
                </div>
              </div>

              <div className="flex justify-end">
                <a
                  href={`/reports?creator=${analysisResult.creator?.id}`}
                  className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-indigo-700 transition-colors flex items-center gap-2"
                >
                  <FileText className="w-5 h-5" />
                  View Full Report
                  <TrendingUp className="w-4 h-4" />
                </a>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
