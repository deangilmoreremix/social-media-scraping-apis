from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Platform(str, Enum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    TWITTER = "twitter"


class ContentTheme(BaseModel):
    theme: str
    percentage: float
    examples: List[str] = []


class AudienceDemographics(BaseModel):
    age_range: str = ""
    top_locations: List[str] = []
    gender_split: Dict[str, float] = {}
    interests: List[str] = []


class ScraperData(BaseModel):
    raw_data: Dict[str, Any] = {}
    scraped_at: datetime = Field(default_factory=datetime.now)
    source_actor: str = ""


class Creator(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    platform: Platform
    username: str
    profile_url: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    engagement_rate: Optional[float] = None
    total_posts: Optional[int] = None
    content_themes: List[ContentTheme] = []
    audience_demographics: Optional[AudienceDemographics] = None
    scraped_data: Optional[ScraperData] = None
    profile_image_url: Optional[str] = None
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreatorCreate(BaseModel):
    profile_url: HttpUrl


class CreatorResponse(BaseModel):
    id: str
    platform: str
    username: str
    profile_url: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    follower_count: Optional[int] = None
    engagement_rate: Optional[float] = None
    content_themes: List[Dict] = []
    audience_demographics: Optional[Dict] = None
    created_at: str
