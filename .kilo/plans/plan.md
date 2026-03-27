# Submagic Affiliate Intelligence Platform

## Product Vision

Build an AI-powered Affiliate Intelligence Platform that analyzes creator social media profiles and recommends optimal Submagic affiliate materials for maximum conversion, powered by GPT-5.4's advanced reasoning and computer use capabilities.

---

## Core Features

### 1. Creator Profile Analysis
- Input: Social media URLs (Instagram, TikTok, YouTube, Twitter/X)
- Bulk CSV upload for multiple creators
- Automatic profile scraping using 3,268 social media APIs
- Extract: Follower counts, engagement rates, content themes, posting frequency, audience demographics
- **GPT-5.4 Computer Use**: Can autonomously navigate social media pages to extract data

### 2. AI-Powered Affiliate Matching
- Analyze creator content style and audience using GPT-5.4
- Match with optimal affiliate materials from Submagic's library:
  - Long-form YouTube review scripts
  - Short-form TikTok/Instagram demo templates
  - Email outreach templates
  - Social media post copy
  - Case studies and testimonials
- Generate "Campaign Score Card" with metrics:
  - Audience Match Score (0-100)
  - Content Fit Score (0-100)
  - Conversion Potential Score (0-100)
- **GPT-5.4 Reasoning**: Adjustable effort levels for optimal cost/quality tradeoff

### 3. Report Generation
- Interactive web dashboard showing:
  - Creator profile summary
  - Recommended affiliate materials ranked by fit
  - Why each material works (AI reasoning)
  - Suggested posting schedule
- PDF export with all recommendations
- **GPT-5.4 Native PDF Generation**: Can generate PDF creation code directly

### 4. Affiliate Material Library
- Curated collection of Submagic affiliate assets
- Categorized by: Platform (YouTube, TikTok, IG), Content Type (Review, Tutorial, Demo), Audience Size
- GPT-5.4 can suggest and generate new material variations

### 5. Advanced Automation (GPT-5.4 Computer Use)
- Automated outreach message generation
- Can navigate affiliate dashboards
- Automated report compilation
- Smart follow-up recommendations

---

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Next.js 15 + React + Tailwind CSS | Modern, fast, SEO-friendly |
| Backend | FastAPI (Python) | High-performance async |
| **AI/LLM** | **GPT-5.4** | **Industry-leading, native computer use, 1M+ token context** |
| **Image Gen** | **DALL-E 3 (via GPT-5.4)** | **Native integration, best quality** |
| Database | PostgreSQL (Supabase) | Scalable, real-time |
| Social APIs | Apify APIs (3,268 available) | Comprehensive social data |
| Auth | Clerk | Simple, secure |
| Deployment | Vercel (frontend) + Railway (backend) | Fast, reliable |
| File Storage | Supabase Storage | Integrated |

---

## GPT-5.4 Specific Capabilities

### Reasoning Effort Control
```python
# Different tasks = different reasoning levels
LOW_EFFORT = "none"      # Simple formatting, extractions
MEDIUM_EFFORT = "medium"  # Default, most tasks
HIGH_EFFORT = "high"      # Complex analysis, multi-step logic
XHIGH_EFFORT = "xhigh"   # Research, strategy generation

# Example:
response = client.chat.completions.create(
    model="gpt-5.4",
    reasoning={"effort": "high"},
    messages=[{"role": "user", "content": "Analyze creator and recommend materials..."}]
)
```

### Native Computer Use
```python
# GPT-5.4 can autonomously:
# - Navigate websites and extract data
# - Fill forms and interact with UIs
# - Create and edit documents
# - Run verification loops

response = client.chat.completions.create(
    model="gpt-5.4",
    tools=[{"type": "computer_use"}],
    messages=[{
        "role": "user",
        "content": "Extract this creator's profile data from their Instagram page"
    }]
)
```

### 1M+ Token Context
- Process entire creator histories in one request
- Compare against full affiliate material library
- Generate comprehensive long-form reports

### Tool Search
- Efficiently works with 100+ affiliate materials
- 47% fewer tokens when matching tools to tasks
- Perfect for large material libraries

---

## Database Schema

### Tables:

**creators**
- id (uuid, pk)
- platform (enum: instagram, tiktok, youtube, twitter)
- username
- profile_url
- follower_count
- engagement_rate
- content_themes (jsonb)
- audience_demographics (jsonb)
- scraped_data (jsonb)
- created_at, updated_at

**affiliate_materials**
- id (uuid, pk)
- name
- description
- platform_target
- content_type
- template_content (text)
- assets_urls (jsonb)
- best_for_audience_size
- best_for_niche

**reports**
- id (uuid, pk)
- creator_id (fk)
- overall_score
- recommendations (jsonb)
- campaign_score_card (jsonb)
- pdf_url
- created_at

**users**
- id (uuid, pk)
- email
- role (admin, affiliate_manager)
- created_at

---

## API Endpoints

### Creator Analysis
- `POST /api/creators/analyze` - Analyze single creator (GPT-5.4)
- `POST /api/creators/bulk-analyze` - Bulk CSV upload and analyze
- `GET /api/creators/:id` - Get creator profile
- `GET /api/creators` - List all creators

### Reports
- `POST /api/reports/generate` - Generate report for creator (GPT-5.4)
- `GET /api/reports/:id` - Get report
- `GET /api/reports/:id/pdf` - Download PDF
- `GET /api/reports` - List reports

### Affiliate Materials
- `GET /api/materials` - List all materials
- `GET /api/materials/:id` - Get specific material
- `POST /api/materials/suggest` - GPT-5.4 suggests new variations

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up Next.js + FastAPI project structure
- [ ] Configure Supabase database
- [ ] Set up Clerk authentication
- [ ] Create base UI components
- [ ] **Set up GPT-5.4 API integration with reasoning effort control**

### Phase 2: Creator Analysis (Week 2)
- [ ] Build Apify API integration layer
- [ ] Implement Instagram profile scraper
- [ ] Implement TikTok profile scraper
- [ ] Implement YouTube channel scraper
- [ ] Create creator data models and storage
- [ ] Build creator input UI (single URL + CSV upload)
- [ ] **Implement GPT-5.4 Computer Use for data extraction**

### Phase 3: AI Matching Engine (Week 3)
- [ ] Design prompt engineering for GPT-5.4 affiliate matching
- [ ] Implement adjustable reasoning effort levels
- [ ] Build GPT-5.4 integration for analysis
- [ ] Create Campaign Score Card algorithm
- [ ] Implement recommendation ranking system
- [ ] Add reasoning explanations with Chain-of-Thought

### Phase 4: Reporting (Week 4)
- [ ] Build interactive report dashboard
- [ ] Implement PDF generation (GPT-5.4 can generate code + libraries)
- [ ] Create Campaign Score Card UI with animated gauges
- [ ] Add recommendation cards with explanations
- [ ] Build report sharing/export features

### Phase 5: Advanced Features & Deploy (Week 5)
- [ ] **Implement GPT-5.4 Tool Search for material matching**
- [ ] **Add computer use for automated outreach**
- [ ] Add error handling and retries
- [ ] Implement rate limiting
- [ ] Add loading states and animations
- [ ] Deploy to Vercel + Railway

---

## Key Libraries

### Frontend
- next: ^15.x
- react: ^19.x
- tailwindcss: ^4.x
- @clerk/nextjs: ^6.x
- lucide-react: icons
- recharts: data visualization

### Backend
- fastapi: ^0.115.x
- pydantic: ^2.x
- openai: ^1.x (GPT-5.4)
- supabase-py: ^2.x
- httpx: async API calls
- python-multipart: file uploads

### AI/PDF
- openai: **GPT-5.4** (replaces GPT-4o, Gemini, Google ADK)
- reportlab/weasyprint: PDF generation
- DALL-E 3: Image generation (via openai SDK)

---

## Environment Variables

```
# Frontend
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_API_URL=

# Backend
OPENAI_API_KEY=              # Required for GPT-5.4
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
APIFY_API_TOKEN=
CLERK_SECRET_KEY=
```

---

## Project Structure

```
submagic-affiliate-intelligence/
├── frontend/
│   ├── app/
│   │   ├── (dashboard)/
│   │   │   ├── creators/
│   │   │   ├── reports/
│   │   │   └── materials/
│   │   ├── api/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── creators/
│   │   ├── reports/
│   │   └── dashboard/
│   ├── lib/
│   │   ├── supabase.ts
│   │   └── utils.ts
│   └── types/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── creators.py
│   │   │   ├── reports.py
│   │   │   └── materials.py
│   │   ├── services/
│   │   │   ├── apify_service.py
│   │   │   ├── gpt54_service.py      # GPT-5.4 integration
│   │   │   ├── pdf_service.py
│   │   │   └── creator_analysis.py
│   │   └── models/
│   │       ├── creator.py
│   │       ├── report.py
│   │       └── material.py
│   ├── requirements.txt
│   └── Dockerfile
├── .kilo/
│   └── plans/
│       └── plan.md
└── README.md
```

---

## GPT-5.4 Pricing Estimates

| Task | Reasoning Effort | Est. Tokens | Cost per 1K calls |
|------|-----------------|-------------|-------------------|
| Simple extraction | none | 500 | $0.01 |
| Profile analysis | medium | 5K | $0.10 |
| Complex matching | high | 20K | $0.40 |
| Full report gen | xhigh | 50K | $1.00 |

**Estimated cost per full analysis**: $0.50-1.50
**Monthly (1K analyses)**: $500-1,500

---

## Success Metrics

- Analyze creator profile in < 30 seconds (GPT-5.4 is 47% more token-efficient)
- Generate complete report in < 60 seconds
- Support bulk uploads of 100+ creators
- 95%+ accuracy on affiliate material recommendations
- 50%+ reduction in token usage vs previous models

---

## Future Enhancements

- Integration with Submagic affiliate API for real-time commission tracking
- A/B testing recommendations
- **GPT-5.4 Computer Use for automated outreach**
- **GPT-5.4 Tool Search for smarter material matching**
- Performance tracking dashboard
- Multi-language support
- DALL-E 3 integration for custom material images

---

## Comparison: GPT-5.4 vs Original Stack

| Feature | Original (Gemini) | New (GPT-5.4) |
|---------|-------------------|----------------|
| Text Gen | ✅ | ✅ Better |
| Image Gen | Gemini Interleaved | DALL-E 3 (Better) |
| Video Gen | Veo 2 | Sora API (Comparable) |
| TTS | Google Cloud TTS | OpenAI TTS (Comparable) |
| Computer Use | ❌ | ✅ Native (75% OSWorld!) |
| Reasoning Control | ❌ | ✅ 5 levels |
| Tool Search | Via ADK | Native (47% fewer tokens) |
| Context | ~1M | 1.05M |
| API Simplicity | Complex (multiple services) | Single SDK |

**Verdict**: GPT-5.4 replaces ALL Google services with better or comparable capabilities, plus adds computer use that Google doesn't have.
