from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import os
from .services.gpt54_service import GPT54Service
from .services.scraper_service import ScraperService
from .services.pdf_service import PDFService

app = FastAPI(
    title="Submagic Affiliate Intelligence",
    description="AI-powered affiliate material recommendations powered by GPT-5.4",
    version="1.0.0"
)

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt54_service = GPT54Service()
scraper_service = ScraperService()
pdf_service = PDFService()


class AnalyzeRequest(BaseModel):
    platform: str
    username: str
    tone: str = "professional"


@app.get("/")
async def root():
    index_path = os.path.join(os.path.dirname(__file__), "../../frontend/index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "Submagic Affiliate Intelligence",
        "status": "running",
        "ai": "GPT-5.4",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


async def generate_sse_events(platform: str, username: str, tone: str):
    """Generator function for SSE streaming analysis results."""
    
    async def send_event(data: dict, event_type: str = "message"):
        yield f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
    
    # Step 1: Scraping Profile
    await asyncio.sleep(0.5)
    async for chunk in send_event({
        "step": "PROFILE",
        "status": "scraping",
        "message": f"Scraping {platform} profile for @{username}..."
    }, "progress"):
        yield chunk
    
    try:
        profile_data = await scraper_service.scrape_profile(platform, username)
    except Exception:
        profile_data = scraper_service._generate_mock_profile(platform, username)
    
    await asyncio.sleep(0.3)
    async for chunk in send_event({
        "step": "PROFILE",
        "status": "complete",
        "data": profile_data
    }, "result"):
        yield chunk
    
    # Step 2: AI Analysis
    await asyncio.sleep(0.5)
    async for chunk in send_event({
        "step": "ANALYSIS",
        "status": "analyzing",
        "message": "GPT-5.4 analyzing audience and content fit..."
    }, "progress"):
        yield chunk
    
    try:
        analysis_result = await gpt54_service.analyze_with_ai(profile_data, tone)
    except Exception:
        analysis_result = gpt54_service._generate_mock_analysis(platform, username, tone)
    
    await asyncio.sleep(0.3)
    async for chunk in send_event({
        "step": "ANALYSIS",
        "status": "complete",
        "data": analysis_result
    }, "result"):
        yield chunk
    
    # Step 3: Materials
    await asyncio.sleep(0.5)
    async for chunk in send_event({
        "step": "MATERIALS",
        "status": "matching",
        "message": "Matching optimal affiliate materials..."
    }, "progress"):
        yield chunk
    
    materials = gpt54_service._get_recommendations(profile_data, tone)
    
    await asyncio.sleep(0.3)
    async for chunk in send_event({
        "step": "MATERIALS",
        "status": "complete",
        "data": {"recommendations": materials}
    }, "result"):
        yield chunk
    
    # Step 4: Strategy
    await asyncio.sleep(0.5)
    async for chunk in send_event({
        "step": "STRATEGY",
        "status": "generating",
        "message": "Generating campaign strategy..."
    }, "progress"):
        yield chunk
    
    strategy = gpt54_service._generate_strategy(profile_data, analysis_result, materials)
    
    await asyncio.sleep(0.3)
    async for chunk in send_event({
        "step": "STRATEGY",
        "status": "complete",
        "data": strategy
    }, "result"):
        yield chunk
    
    # Complete
    async for chunk in send_event({
        "status": "complete",
        "message": "Analysis complete!"
    }, "complete"):
        yield chunk


@app.post("/analyze/stream")
async def analyze_stream(request: AnalyzeRequest):
    """
    Analyze a creator with SSE streaming.
    """
    return StreamingResponse(
        generate_sse_events(request.platform, request.username, request.tone),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/analyze")
async def analyze_creator(request: AnalyzeRequest):
    """
    Analyze a creator (non-streaming).
    """
    try:
        profile_data = await scraper_service.scrape_profile(request.platform, request.username)
    except Exception:
        profile_data = scraper_service._generate_mock_profile(request.platform, request.username)
    
    try:
        analysis_result = await gpt54_service.analyze_with_ai(profile_data, request.tone)
    except Exception:
        analysis_result = gpt54_service._generate_mock_analysis(request.platform, request.username, request.tone)
    
    return {
        "profile": profile_data,
        "analysis": analysis_result
    }


@app.post("/download")
async def download_report(request: Request):
    """
    Generate PDF report from analysis data.
    """
    body = await request.json()
    pdf_bytes = await pdf_service.generate_report(body)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=affiliate-report.pdf"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
