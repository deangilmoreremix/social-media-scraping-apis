# Submagic Affiliate Intelligence Platform

## Product Vision

Build an AI-powered Affiliate Intelligence Platform that analyzes creator social media profiles and recommends optimal Submagic affiliate materials for maximum conversion.

---

## Core Features

### 1. Creator Profile Analysis
- Input: Social media URLs (Instagram, TikTok, YouTube, Twitter/X)
- Bulk CSV upload for multiple creators
- Automatic profile scraping using 3,268 social media APIs
- Extract: Follower counts, engagement rates, content themes, posting frequency, audience demographics

### 2. AI-Powered Affiliate Matching
- Analyze creator content style and audience
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

### 3. Report Generation
- Interactive web dashboard showing:
  - Creator profile summary
  - Recommended affiliate materials ranked by fit
  - Why each material works (AI reasoning)
  - Suggested posting schedule
- PDF export with all recommendations

### 4. Affiliate Material Library
- Curated collection of Submagic affiliate assets
- Categorized by: Platform (YouTube, TikTok, IG), Content Type (Review, Tutorial, Demo), Audience Size

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15 + React + Tailwind CSS + shadcn/ui |
| Backend | FastAPI (Python) |
| AI/LLM | OpenAI GPT-4o |
| Database | PostgreSQL (Supabase) |
| Social APIs | Apify APIs (3,268 available) |
| Auth | Clerk |
| Deployment | Vercel (frontend) + Railway (backend) |
| File Storage | Supabase Storage |

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
- `POST /api/creators/analyze` - Analyze single creator
- `POST /api/creators/bulk-analyze` - Bulk CSV upload and analyze
- `GET /api/creators/:id` - Get creator profile
- `GET /api/creators` - List all creators

### Reports
- `POST /api/reports/generate` - Generate report for creator
- `GET /api/reports/:id` - Get report
- `GET /api/reports/:id/pdf` - Download PDF
- `GET /api/reports` - List reports

### Affiliate Materials
- `GET /api/materials` - List all materials
- `GET /api/materials/:id` - Get specific material

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up Next.js + FastAPI project structure
- [ ] Configure Supabase database
- [ ] Set up Clerk authentication
- [ ] Create base UI components with shadcn/ui
- [ ] Set up OpenAI API integration

### Phase 2: Creator Analysis (Week 2)
- [ ] Build Apify API integration layer
- [ ] Implement Instagram profile scraper
- [ ] Implement TikTok profile scraper
- [ ] Implement YouTube channel scraper
- [ ] Create creator data models and storage
- [ ] Build creator input UI (single URL + CSV upload)

### Phase 3: AI Matching Engine (Week 3)
- [ ] Design prompt engineering for affiliate matching
- [ ] Build GPT-4o integration for analysis
- [ ] Create Campaign Score Card algorithm
- [ ] Implement recommendation ranking system
- [ ] Add reasoning explanations

### Phase 4: Reporting (Week 4)
- [ ] Build interactive report dashboard
- [ ] Implement PDF generation
- [ ] Create Campaign Score Card UI
- [ ] Add recommendation cards with explanations
- [ ] Build report sharing/export features

### Phase 5: Polish & Deploy (Week 5)
- [ ] Add error handling and retries
- [ ] Implement rate limiting
- [ ] Add loading states and animations
- [ ] Deploy to Vercel + Railway
- [ ] Performance optimization

---

## Key Libraries

### Frontend
- next: ^15.x
- react: ^19.x
- tailwindcss: ^4.x
- shadcn/ui components
- @clerk/nextjs: ^6.x
- lucide-react: icons

### Backend
- fastapi: ^0.115.x
- pydantic: ^2.x
- openai: ^1.x
- supabase-py: ^2.x
- httpx: for API calls
- python-multipart: for file uploads

### AI/PDF
- openai: GPT-4o integration
- reportlab or weasyprint: PDF generation

---

## Environment Variables

```
# Frontend
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_API_URL=

# Backend
OPENAI_API_KEY=
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
│   │   ├── ui/           # shadcn components
│   │   ├── creators/     # Creator-related components
│   │   ├── reports/      # Report components
│   │   └── dashboard/    # Dashboard layout
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
│   │   │   ├── openai_service.py
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

## Success Metrics

- Analyze creator profile in < 30 seconds
- Generate complete report in < 60 seconds
- Support bulk uploads of 100+ creators
- 95%+ accuracy on affiliate material recommendations

---

## Future Enhancements

- Integration with Submagic affiliate API for real-time commission tracking
- A/B testing recommendations
- Creator outreach automation
- Performance tracking dashboard
- Multi-language support
