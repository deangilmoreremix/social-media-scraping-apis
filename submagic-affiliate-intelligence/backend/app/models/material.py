from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class PlatformTarget(str, Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    EMAIL = "email"
    BLOG = "blog"
    ALL = "all"


class ContentType(str, Enum):
    REVIEW = "review"
    TUTORIAL = "tutorial"
    DEMO = "demo"
    TESTIMONIAL = "testimonial"
    COMPARISON = "comparison"
    UNBOXING = "unboxing"
    SPONSORED_POST = "sponsored_post"
    EMAIL_TEMPLATE = "email_template"


class Material(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    platform_target: PlatformTarget
    content_type: ContentType
    template_content: Optional[str] = None
    assets_urls: List[str] = []
    best_for_audience_size: List[str] = []  # micro, small, medium, large
    best_for_niche: List[str] = []
    conversion_tips: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)


class MaterialCreate(BaseModel):
    name: str
    description: str
    platform_target: PlatformTarget
    content_type: ContentType
    template_content: Optional[str] = None
    assets_urls: List[str] = []
    best_for_audience_size: List[str] = []
    best_for_niche: List[str] = []
    conversion_tips: List[str] = []


class MaterialResponse(BaseModel):
    id: str
    name: str
    description: str
    platform_target: str
    content_type: str
    template_content: Optional[str] = None
    assets_urls: List[str]
    best_for_audience_size: List[str]
    best_for_niche: List[str]
    conversion_tips: List[str]
    created_at: str
