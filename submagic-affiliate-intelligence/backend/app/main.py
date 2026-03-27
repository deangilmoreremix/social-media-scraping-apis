from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import creators, reports, materials

app = FastAPI(
    title="Submagic Affiliate Intelligence API",
    description="AI-powered affiliate material recommendations for Submagic creators",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(creators.router, prefix="/api/creators", tags=["creators"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(materials.router, prefix="/api/materials", tags=["materials"])


@app.get("/")
async def root():
    return {"message": "Submagic Affiliate Intelligence API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
