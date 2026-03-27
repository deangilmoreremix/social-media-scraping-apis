from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4


class ScoreCard(BaseModel):
    audience_match_score: int = Field(ge=0, le=100, description="How well the creator's audience matches Submagic's target audience")
    content_fit_score: int = Field(ge=0, le=100, description="How well the creator's content style fits with Submagic's brand")
    conversion_potential_score: int = Field(ge=0, le=100, description="Estimated conversion potential based on historical data")
    overall_score: int = Field(ge=0, le=100, description="Weighted average of all scores")
    reasoning: Dict[str, str] = Field(default_factory=dict, description="AI reasoning for each score")


class Recommendation(BaseModel):
    material_id: str
    material_name: str
    platform: str
    content_type: str
    match_score: int
    reasoning: str
    suggested_posting_times: List[str] = []
    tips_for_maximum_engagement: List[str] = []


class Report(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    creator_id: UUID
    creator_username: str
    creator_platform: str
    overall_score: int
    score_card: ScoreCard
    recommendations: List[Recommendation]
    executive_summary: str
    pdf_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class ReportCreate(BaseModel):
    creator_id: str


class ReportResponse(BaseModel):
    id: str
    creator_id: str
    creator_username: str
    creator_platform: str
    overall_score: int
    score_card: Dict
    recommendations: List[Dict]
    executive_summary: str
    pdf_url: Optional[str] = None
    created_at: str
