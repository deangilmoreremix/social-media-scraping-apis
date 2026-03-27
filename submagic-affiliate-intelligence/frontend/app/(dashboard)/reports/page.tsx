"use client";

import { useState, useEffect } from "react";
import { 
  BarChart3, 
  FileText, 
  Download,
  Loader2,
  TrendingUp,
  Users,
  Target,
  Zap,
  ArrowUpRight,
  Instagram,
  Youtube
} from "lucide-react";

const MOCK_REPORTS = [
  {
    id: "1",
    creator_username: "productivity_guru",
    creator_platform: "instagram",
    overall_score: 87,
    created_at: "2026-03-27T10:00:00Z",
  },
  {
    id: "2",
    creator_username: "techreviewer_pro",
    creator_platform: "youtube",
    overall_score: 92,
    created_at: "2026-03-26T15:30:00Z",
  },
  {
    id: "3",
    creator_username: "social_media_tips",
    creator_platform: "instagram",
    overall_score: 78,
    created_at: "2026-03-25T09:15:00Z",
  },
];

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [selectedReport, setSelectedReport] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setReports(MOCK_REPORTS);
      setIsLoading(false);
    }, 1000);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 85) return "text-green-600 bg-green-50";
    if (score >= 70) return "text-indigo-600 bg-indigo-50";
    if (score >= 50) return "text-yellow-600 bg-yellow-50";
    return "text-red-600 bg-red-50";
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Reports</h1>
        <p className="text-slate-600">
          View and download AI-generated affiliate material recommendations
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <div className="p-4 border-b border-slate-100">
              <h2 className="font-semibold text-slate-900">Recent Reports</h2>
            </div>
            <div className="divide-y divide-slate-100">
              {reports.map((report) => (
                <button
                  key={report.id}
                  onClick={() => setSelectedReport(report)}
                  className={`w-full p-4 text-left hover:bg-slate-50 transition-colors ${
                    selectedReport?.id === report.id ? "bg-indigo-50" : ""
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      {report.creator_platform === "instagram" && (
                        <Instagram className="w-4 h-4 text-pink-500" />
                      )}
                      {report.creator_platform === "youtube" && (
                        <Youtube className="w-4 h-4 text-red-500" />
                      )}
                      <span className="font-medium">@{report.creator_username}</span>
                    </div>
                    <span className={`text-sm font-semibold px-2 py-0.5 rounded-full ${getScoreColor(report.overall_score)}`}>
                      {report.overall_score}
                    </span>
                  </div>
                  <p className="text-sm text-slate-500 mt-1">
                    {formatDate(report.created_at)}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedReport ? (
            <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
              <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold">Report for @{selectedReport.creator_username}</h2>
                  <p className="text-slate-500">{formatDate(selectedReport.created_at)}</p>
                </div>
                <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2">
                  <Download className="w-4 h-4" />
                  Download PDF
                </button>
              </div>

              <div className="p-6 space-y-8">
                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-indigo-600" />
                    Campaign Score Card
                  </h3>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl p-5 text-center">
                      <div className="text-4xl font-bold text-indigo-600 mb-2">87</div>
                      <div className="text-sm font-medium text-slate-700">Audience Match</div>
                      <p className="text-xs text-slate-500 mt-1">High alignment with target</p>
                    </div>
                    <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-5 text-center">
                      <div className="text-4xl font-bold text-green-600 mb-2">92</div>
                      <div className="text-sm font-medium text-slate-700">Content Fit</div>
                      <p className="text-xs text-slate-500 mt-1">Perfect style match</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-5 text-center">
                      <div className="text-4xl font-bold text-purple-600 mb-2">85</div>
                      <div className="text-sm font-medium text-slate-700">Conversion</div>
                      <p className="text-xs text-slate-500 mt-1">Strong potential</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <Target className="w-5 h-5 text-indigo-600" />
                    Top Recommendations
                  </h3>
                  
                  <div className="space-y-4">
                    {[
                      {
                        name: "Instagram Reels Tutorial",
                        platform: "instagram",
                        score: 92,
                        reason: "Your Reels-focused content style aligns perfectly with Submagic's tutorial format.",
                        tips: ["Use clear UI demonstrations", "Add trending audio", "Include before/after"]
                      },
                      {
                        name: "TikTok Demo Hook",
                        platform: "tiktok",
                        score: 88,
                        reason: "Your short-form video expertise makes this quick demo format ideal.",
                        tips: ["Hook in first 2 seconds", "Show transformation", "Use text overlays"]
                      }
                    ].map((rec, i) => (
                      <div key={i} className="border border-slate-200 rounded-xl p-5">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h4 className="font-semibold">{rec.name}</h4>
                            <p className="text-sm text-slate-500 capitalize">{rec.platform}</p>
                          </div>
                          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
                            {rec.score}% Match
                          </span>
                        </div>
                        <p className="text-slate-600 mb-4">{rec.reason}</p>
                        <div>
                          <p className="text-sm font-medium text-slate-700 mb-2">Engagement Tips:</p>
                          <ul className="space-y-1">
                            {rec.tips.map((tip, j) => (
                              <li key={j} className="text-sm text-slate-600 flex items-center gap-2">
                                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full" />
                                {tip}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-indigo-600" />
                    Executive Summary
                  </h3>
                  <div className="bg-slate-50 rounded-xl p-5">
                    <p className="text-slate-700 leading-relaxed">
                      Based on our analysis of @{selectedReport.creator_username}&apos;s Instagram profile, 
                      we recommend focusing on short-form tutorial content. Your audience 
                      (primarily content creators and businesses) represents Submagic&apos;s ideal 
                      customer base. The recommended materials are tailored to maximize 
                      engagement and conversion based on historical performance data.
                    </p>
                    <div className="mt-4 pt-4 border-t border-slate-200 flex items-center gap-2 text-sm text-slate-500">
                      <TrendingUp className="w-4 h-4" />
                      Estimated conversion rate: <span className="font-semibold text-green-600">4.2%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
              <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-700 mb-2">No Report Selected</h3>
              <p className="text-slate-500">
                Select a report from the list to view details
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
