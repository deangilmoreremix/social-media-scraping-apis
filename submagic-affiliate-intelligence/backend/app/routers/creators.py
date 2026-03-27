from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from ..models.creator import CreatorCreate, CreatorResponse, Platform
from ..services.apify_service import ApifyService
from ..services.creator_analysis import CreatorAnalysisService

router = APIRouter()
apify_service = ApifyService()
creator_analysis_service = CreatorAnalysisService()


@router.post("/analyze", response_model=dict)
async def analyze_creator(creator_data: CreatorCreate):
    """Analyze a single creator from their profile URL"""
    try:
        result = await creator_analysis_service.analyze_profile(str(creator_data.profile_url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-analyze", response_model=dict)
async def bulk_analyze_creators(file: UploadFile = File(...)):
    """Bulk analyze creators from a CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        content = await file.read()
        result = await creator_analysis_service.bulk_analyze(content.decode('utf-8'))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{creator_id}", response_model=dict)
async def get_creator(creator_id: str):
    """Get a creator by ID"""
    try:
        creator = await creator_analysis_service.get_creator(creator_id)
        if not creator:
            raise HTTPException(status_code=404, detail="Creator not found")
        return creator
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def list_creators(
    platform: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """List all creators with optional filtering"""
    try:
        creators = await creator_analysis_service.list_creators(
            platform=platform,
            limit=limit,
            offset=offset
        )
        return {"creators": creators, "count": len(creators)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
