"use client";

import { useState, useEffect } from "react";
import { 
  FileText, 
  Filter,
  Instagram,
  Youtube,
  Mail,
  Search,
  Loader2,
  Copy,
  Check
} from "lucide-react";

const MATERIALS = [
  {
    id: "mat_1",
    name: "Submagic Review Script - Long Form",
    description: "Comprehensive review script for YouTube videos (5-10 minutes)",
    platform_target: "youtube",
    content_type: "review",
    best_for_audience_size: ["medium", "large"],
    conversion_tips: ["Show real before/after examples", "Mention time saved specifically", "Address the price point directly"]
  },
  {
    id: "mat_2",
    name: "TikTok Demo Hook",
    description: "15-30 second hook video showcasing Submagic's AI captions",
    platform_target: "tiktok",
    content_type: "demo",
    best_for_audience_size: ["micro", "small", "medium"],
    conversion_tips: ["Keep it under 30 seconds", "Focus on one feature", "Use trending sounds"]
  },
  {
    id: "mat_3",
    name: "Instagram Reels Tutorial",
    description: "Step-by-step tutorial for creating engaging Reels with Submagic",
    platform_target: "instagram",
    content_type: "tutorial",
    best_for_audience_size: ["small", "medium"],
    conversion_tips: ["Use step-by-step text overlays", "Show the UI clearly", "End with a clear CTA"]
  },
  {
    id: "mat_4",
    name: "Email Outreach Template",
    description: "Professional email template for cold outreach to potential affiliates",
    platform_target: "email",
    content_type: "email_template",
    best_for_audience_size: ["small", "medium", "large"],
    conversion_tips: ["Personalize with specific content examples", "Highlight the recurring commission", "Make it easy to respond"]
  },
  {
    id: "mat_5",
    name: "Comparison Post Template",
    description: "Comparison content vs other video editing tools",
    platform_target: "youtube",
    content_type: "comparison",
    best_for_audience_size: ["medium", "large"],
    conversion_tips: ["Be honest about pros/cons", "Focus on unique Submagic features", "Use timestamps for better UX"]
  },
  {
    id: "mat_6",
    name: "Success Story Template",
    description: "Share how Submagic helped transform your content",
    platform_target: "blog",
    content_type: "testimonial",
    best_for_audience_size: ["medium", "large"],
    conversion_tips: ["Use specific numbers and metrics", "Include personal anecdotes", "Add embedded demo video"]
  }
];

const PLATFORM_ICONS: Record<string, React.ReactNode> = {
  instagram: <Instagram className="w-4 h-4 text-pink-500" />,
  youtube: <Youtube className="w-4 h-4 text-red-500" />,
  tiktok: <span className="text-sm">🎵</span>,
  email: <Mail className="w-4 h-4 text-slate-500" />,
  blog: <FileText className="w-4 h-4 text-indigo-500" />,
};

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<any[]>([]);
  const [filteredMaterials, setFilteredMaterials] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedMaterial, setSelectedMaterial] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [platformFilter, setPlatformFilter] = useState<string>("all");
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    setTimeout(() => {
      setMaterials(MATERIALS);
      setFilteredMaterials(MATERIALS);
      setIsLoading(false);
    }, 500);
  }, []);

  useEffect(() => {
    let filtered = materials;
    
    if (searchQuery) {
      filtered = filtered.filter(m => 
        m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    if (platformFilter !== "all") {
      filtered = filtered.filter(m => m.platform_target === platformFilter);
    }
    
    setFilteredMaterials(filtered);
  }, [searchQuery, platformFilter, materials]);

  const handleCopy = async (text: string, id: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
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
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Affiliate Materials</h1>
        <p className="text-slate-600">
          Browse and copy pre-built templates optimized for maximum conversion
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search materials..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-slate-400" />
          <select
            value={platformFilter}
            onChange={(e) => setPlatformFilter(e.target.value)}
            className="px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 outline-none"
          >
            <option value="all">All Platforms</option>
            <option value="instagram">Instagram</option>
            <option value="youtube">YouTube</option>
            <option value="tiktok">TikTok</option>
            <option value="email">Email</option>
            <option value="blog">Blog</option>
          </select>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="space-y-4">
          {filteredMaterials.map((material) => (
            <button
              key={material.id}
              onClick={() => setSelectedMaterial(material)}
              className={`w-full text-left bg-white rounded-xl border p-5 transition-all hover:border-indigo-200 hover:shadow-md ${
                selectedMaterial?.id === material.id ? "border-indigo-500 ring-2 ring-indigo-500/20" : "border-slate-200"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  {PLATFORM_ICONS[material.platform_target]}
                  <div>
                    <h3 className="font-semibold text-slate-900">{material.name}</h3>
                    <p className="text-sm text-slate-500 mt-1">{material.description}</p>
                    <div className="flex gap-2 mt-3">
                      <span className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-full capitalize">
                        {material.content_type.replace("_", " ")}
                      </span>
                      <span className="text-xs bg-indigo-100 text-indigo-600 px-2 py-1 rounded-full">
                        {material.best_for_audience_size.join(", ")}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>

        <div className="lg:sticky lg:top-24">
          {selectedMaterial ? (
            <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
              <div className="p-5 border-b border-slate-100 bg-slate-50">
                <div className="flex items-center gap-2 mb-2">
                  {PLATFORM_ICONS[selectedMaterial.platform_target]}
                  <h2 className="text-lg font-semibold">{selectedMaterial.name}</h2>
                </div>
                <p className="text-sm text-slate-600">{selectedMaterial.description}</p>
              </div>
              
              <div className="p-5 space-y-6">
                <div>
                  <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Template Content
                  </h3>
                  <div className="bg-slate-50 rounded-xl p-4 relative group">
                    <pre className="text-sm text-slate-700 whitespace-pre-wrap font-mono">
                      {selectedMaterial.content_type === "email_template" 
                        ? `SUBJECT: Partnership Opportunity - Earn 30% recurring commission

Hi [NAME],

I came across your [PLATFORM] content and loved your approach to [NICHE]. 

I'm reaching out from Submagic - the #1 AI video editing tool trusted by 3M+ creators. We'd love to have you join our affiliate program.

What makes us different:
- 30% recurring commission (lifetime)
- No limit on earnings
- High-converting product your audience will love

Would you be open to a quick 15-minute call?

Best,
[YOUR_NAME]
Submagic Partnerships`
                        : `HOOK: "POV: You just discovered the AI that edits your videos for you"

[Show quick before/after demo]

KEY POINTS:
- AI-powered captions
- Auto-editing features  
- Save hours per video

CTA: Link in bio | Use code [AFFILIATE_CODE] for discount`
                      }
                    </pre>
                    <button
                      onClick={() => handleCopy(selectedMaterial.id, selectedMaterial.id)}
                      className="absolute top-2 right-2 p-2 bg-white rounded-lg shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      {copiedId === selectedMaterial.id ? (
                        <Check className="w-4 h-4 text-green-600" />
                      ) : (
                        <Copy className="w-4 h-4 text-slate-600" />
                      )}
                    </button>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-slate-700 mb-3">
                    Conversion Tips
                  </h3>
                  <ul className="space-y-2">
                    {selectedMaterial.conversion_tips.map((tip: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                        <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full mt-1.5 flex-shrink-0" />
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
              <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-700 mb-2">Select a Material</h3>
              <p className="text-slate-500">
                Click on a material from the list to view its content
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
