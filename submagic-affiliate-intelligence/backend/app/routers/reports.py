from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from ..models.report import ReportCreate, ReportResponse
from ..services.openai_service import OpenAIService
from ..services.pdf_service import PDFService

router = APIRouter()
openai_service = OpenAIService()
pdf_service = PDFService()


@router.post("/generate", response_model=dict)
async def generate_report(report_data: ReportCreate):
    """Generate a report for a creator"""
    try:
        report = await openai_service.generate_affiliate_report(report_data.creator_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}", response_model=dict)
async def get_report(report_id: str):
    """Get a report by ID"""
    try:
        report = await openai_service.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/pdf")
async def download_pdf(report_id: str):
    """Download report as PDF"""
    try:
        pdf_path = await pdf_service.generate_report_pdf(report_id)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"report_{report_id}.pdf"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def list_reports(
    creator_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """List all reports with optional filtering"""
    try:
        reports = await openai_service.list_reports(
            creator_id=creator_id,
            limit=limit,
            offset=offset
        )
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
