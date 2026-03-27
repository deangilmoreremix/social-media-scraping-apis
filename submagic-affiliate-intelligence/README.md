# Submagic Affiliate Intelligence

AI-powered affiliate material recommendations powered by GPT-5.4.

## Features

- Analyze creators across Instagram, TikTok, YouTube, and Twitter
- Match creators with optimal Submagic affiliate materials
- Real-time SSE streaming analysis
- Campaign Score Cards with audience match, content fit, and conversion metrics
- PDF report generation

## Quick Start

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_openai_key
export APIFY_API_TOKEN=your_apify_token  # optional

# Run the server
python -m uvicorn app.main:app --reload --port 8000
```

Or use Docker:

```bash
docker-compose up
```

Then open http://localhost:8000

## API Endpoints

- `POST /analyze/stream` - Analyze creator with SSE streaming
- `POST /analyze` - Analyze creator (non-streaming)
- `POST /download` - Generate PDF report

## Configuration

Set these environment variables:

- `OPENAI_API_KEY` - OpenAI API key for GPT-5.4 (required for AI analysis)
- `APIFY_API_TOKEN` - Apify API token for social media scraping (optional, falls back to mock data)
- `SUPABASE_URL` - Supabase URL (optional)
- `SUPABASE_KEY` - Supabase key (optional)
