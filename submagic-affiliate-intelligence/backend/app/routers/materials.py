from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.material import MaterialCreate, MaterialResponse, PlatformTarget, ContentType

router = APIRouter()

AFFILIATE_MATERIALS = [
    {
        "id": "mat_1",
        "name": "Submagic Review Script - Long Form",
        "description": "Comprehensive review script for YouTube videos (5-10 minutes)",
        "platform_target": "youtube",
        "content_type": "review",
        "template_content": "OPENING: Start with a hook about how much time you spend editing videos...\n\nKEY POINTS TO COVER:\n1. AI-powered captions (show before/after)\n2. Auto-editing features\n3. B-roll and transitions\n4. Time saved\n\nCTA: Use my affiliate link for 20% off first month",
        "assets_urls": ["https://submagic.co/before-after-demo.mp4"],
        "best_for_audience_size": ["medium", "large"],
        "best_for_niche": ["tech review", "productivity", "content creation"],
        "conversion_tips": ["Show real before/after examples", "Mention time saved specifically", "Address the price point directly"]
    },
    {
        "id": "mat_2",
        "name": "TikTok Demo Hook",
        "description": "15-30 second hook video showcasing Submagic's AI captions",
        "platform_target": "tiktok",
        "content_type": "demo",
        "template_content": "HOOK: \"POV: You just discovered the AI that edits your videos for you\"\n\nDEMO: Show quick before/after of caption generation\n\nCTA: Link in bio | Use code [AFFILIATE_CODE] for discount",
        "assets_urls": ["https://submagic.co/brand-kit.zip"],
        "best_for_audience_size": ["micro", "small", "medium"],
        "best_for_niche": ["content creation", "social media", "small business"],
        "conversion_tips": ["Keep it under 30 seconds", "Focus on one feature", "Use trending sounds"]
    },
    {
        "id": "mat_3",
        "name": "Instagram Reels Tutorial",
        "description": "Step-by-step tutorial for creating engaging Reels with Submagic",
        "platform_target": "instagram",
        "content_type": "tutorial",
        "template_content": "HOOK: \"Here's how I add viral captions to my reels in seconds...\"\n\nSTEPS:\n1. Upload your video\n2. Let AI detect key moments\n3. Add auto-generated captions\n4. Export and post\n\nSWIPE UP CTA: Link in bio for free trial",
        "assets_urls": [],
        "best_for_audience_size": ["small", "medium"],
        "best_for_niche": ["lifestyle", "business", "education"],
        "conversion_tips": ["Use step-by-step text overlays", "Show the UI clearly", "End with a clear CTA"]
    },
    {
        "id": "mat_4",
        "name": "Email Outreach Template",
        "description": "Professional email template for cold outreach to potential affiliates",
        "platform_target": "email",
        "content_type": "email_template",
        "template_content": "SUBJECT: Partnership Opportunity - Earn 30% recurring commission\n\nHi [NAME],\n\nI came across your [PLATFORM] content and loved your approach to [NICHE]. \n\nI'm reaching out from Submagic - the #1 AI video editing tool trusted by 3M+ creators. We'd love to have you join our affiliate program.\n\nWhat makes us different:\n- 30% recurring commission (lifetime)\n- No limit on earnings\n- High-converting product your audience will love\n- Dedicated affiliate support\n\nWould you be open to a quick 15-minute call to learn more?\n\nBest,\n[YOUR_NAME]\nSubmagic Partnerships",
        "assets_urls": [],
        "best_for_audience_size": ["small", "medium", "large"],
        "best_for_niche": ["tech", "business", "content creation"],
        "conversion_tips": ["Personalize with specific content examples", "Highlight the recurring commission", "Make it easy to respond"]
    },
    {
        "id": "mat_5",
        "name": "Comparison Post Template",
        "description": "Comparison content vs other video editing tools",
        "platform_target": "youtube",
        "content_type": "comparison",
        "template_content": "TITLE: Submagic vs [Competitor] - Which AI Video Editor Wins?\n\nSECTIONS:\n1. Pricing comparison\n2. Features comparison\n3. Ease of use\n4. AI capabilities\n5. Export quality\n\nVERDICT: [Your honest recommendation with affiliate link]",
        "assets_urls": [],
        "best_for_audience_size": ["medium", "large"],
        "best_for_niche": ["tech review", "productivity", "content creation"],
        "conversion_tips": ["Be honest about pros/cons", "Focus on unique Submagic features", "Use timestamps for better UX"]
    },
    {
        "id": "mat_6",
        "name": "Success Story Template",
        "description": "Share how Submagic helped transform your content",
        "platform_target": "blog",
        "content_type": "testimonial",
        "template_content": "TITLE: How I [SPECIFIC RESULT] with Submagic\n\nSTORY STRUCTURE:\n1. The problem (editing was taking too long)\n2. The solution (discovered Submagic)\n3. The results (specific metrics)\n4. How you use it daily\n5. CTA with affiliate link\n\nINCLUDE: Screenshots, before/after, time saved metrics",
        "assets_urls": [],
        "best_for_audience_size": ["medium", "large"],
        "best_for_niche": ["content creation", "business", "productivity"],
        "conversion_tips": ["Use specific numbers and metrics", "Include personal anecdotes", "Add embedded demo video"]
    }
]


@router.get("/", response_model=dict)
async def list_materials(
    platform: Optional[str] = None,
    content_type: Optional[str] = None,
    audience_size: Optional[str] = None
):
    """List all affiliate materials with optional filtering"""
    materials = AFFILIATE_MATERIALS.copy()
    
    if platform:
        materials = [m for m in materials if m["platform_target"] == platform or m["platform_target"] == "all"]
    
    if content_type:
        materials = [m for m in materials if m["content_type"] == content_type]
    
    if audience_size:
        materials = [m for m in materials if audience_size in m["best_for_audience_size"]]
    
    return {"materials": materials, "count": len(materials)}


@router.get("/{material_id}", response_model=dict)
async def get_material(material_id: str):
    """Get a specific material by ID"""
    for material in AFFILIATE_MATERIALS:
        if material["id"] == material_id:
            return material
    raise HTTPException(status_code=404, detail="Material not found")


@router.post("/", response_model=dict)
async def create_material(material_data: MaterialCreate):
    """Create a new affiliate material (admin only)"""
    new_material = {
        "id": f"mat_{len(AFFILIATE_MATERIALS) + 1}",
        **material_data.model_dump()
    }
    AFFILIATE_MATERIALS.append(new_material)
    return new_material
