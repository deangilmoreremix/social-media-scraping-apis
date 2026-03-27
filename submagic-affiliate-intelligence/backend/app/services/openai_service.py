from openai import OpenAI
from typing import Dict, Any, List
from ..config import get_settings
from ..routers.materials import AFFILIATE_MATERIALS

settings = get_settings()


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    async def generate_affiliate_report(self, creator_id: str) -> Dict[str, Any]:
        """Generate an affiliate report for a creator"""
        creator_data = await self._get_creator_data(creator_id)
        
        if not creator_data:
            return {
                "error": "Creator not found",
                "creator_id": creator_id
            }
        
        if self.client:
            report = await self._generate_ai_report(creator_data)
        else:
            report = self._generate_mock_report(creator_data)
        
        return {
            "creator_id": creator_id,
            "creator_username": creator_data.get("username", "Unknown"),
            "creator_platform": creator_data.get("platform", "unknown"),
            "profile_summary": self._generate_profile_summary(creator_data),
            **report
        }
    
    async def _generate_ai_report(self, creator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use GPT-4o to generate intelligent recommendations"""
        platform = creator_data.get("platform", "social media")
        username = creator_data.get("username", "the creator")
        
        prompt = f"""Analyze this {platform} creator and recommend the best Submagic affiliate materials for them.

Creator Data:
{self._format_creator_data(creator_data)}

Available Affiliate Materials:
{self._format_materials()}

Generate a comprehensive report with:
1. A Campaign Score Card with scores (0-100) for:
   - Audience Match Score (how well their audience matches Submagic's target)
   - Content Fit Score (how well their content style fits Submagic's brand)
   - Conversion Potential Score (based on engagement and audience size)
   - Overall Score (weighted average)

2. Top 3 recommended affiliate materials ranked by match score

3. An executive summary explaining the recommendations

4. Specific tips for maximizing engagement with each recommended material

Return your response as a structured JSON object."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert affiliate marketing strategist specializing in AI tools and short-form video content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _generate_mock_report(self, creator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mock report for development/testing"""
        followers = creator_data.get("follower_count", creator_data.get("followers", 0))
        platform = creator_data.get("platform", "unknown")
        
        audience_match = min(95, max(45, int(followers / 1000)))
        content_fit = min(90, max(50, int(followers / 1200)))
        conversion = min(85, max(40, int(followers / 1500)))
        overall = int((audience_match + content_fit + conversion) / 3)
        
        recommendations = []
        if platform == "instagram":
            recommendations = [
                {
                    "material_id": "mat_3",
                    "material_name": "Instagram Reels Tutorial",
                    "platform": "instagram",
                    "content_type": "tutorial",
                    "match_score": 92,
                    "reasoning": "Your Reels-focused content style aligns perfectly with Submagic's tutorial format. The step-by-step approach works well with your audience.",
                    "suggested_posting_times": ["9 AM EST", "12 PM EST", "7 PM EST"],
                    "tips_for_maximum_engagement": [
                        "Use the 'swipe up' pattern in your captions",
                        "Show the UI clearly with good lighting",
                        "Add trending audio in the background"
                    ]
                },
                {
                    "material_id": "mat_2",
                    "material_name": "TikTok Demo Hook",
                    "platform": "tiktok",
                    "content_type": "demo",
                    "match_score": 88,
                    "reasoning": "Your short-form video expertise makes this quick demo format ideal for your content style.",
                    "suggested_posting_times": ["6 PM EST", "9 PM EST"],
                    "tips_for_maximum_engagement": [
                        "Hook viewers in the first 2 seconds",
                        "Show the transformation clearly",
                        "Use text overlays for key points"
                    ]
                }
            ]
        elif platform == "youtube":
            recommendations = [
                {
                    "material_id": "mat_1",
                    "material_name": "Submagic Review Script - Long Form",
                    "platform": "youtube",
                    "content_type": "review",
                    "match_score": 94,
                    "reasoning": "Your channel's in-depth review style is perfect for this comprehensive review format. The detailed approach resonates with your engaged subscriber base.",
                    "suggested_posting_times": ["2 PM EST (for US)", "10 AM EST (for EU)"],
                    "tips_for_maximum_engagement": [
                        "Include real before/after examples",
                        "Mention specific time savings",
                        "Address the price point head-on"
                    ]
                },
                {
                    "material_id": "mat_5",
                    "material_name": "Comparison Post Template",
                    "platform": "youtube",
                    "content_type": "comparison",
                    "match_score": 87,
                    "reasoning": "Your analytical content style makes comparison videos highly effective for your audience.",
                    "suggested_posting_times": ["11 AM EST", "4 PM EST"],
                    "tips_for_maximum_engagement": [
                        "Be honest about pros and cons",
                        "Use timestamps for easy navigation",
                        "Include a clear verdict"
                    ]
                }
            ]
        else:
            recommendations = [
                {
                    "material_id": "mat_4",
                    "material_name": "Email Outreach Template",
                    "platform": "email",
                    "content_type": "email_template",
                    "match_score": 85,
                    "reasoning": "Direct outreach is effective for creators at your scale looking to expand partnerships.",
                    "suggested_posting_times": ["Tuesday 10 AM EST", "Thursday 2 PM EST"],
                    "tips_for_maximum_engagement": [
                        "Personalize with specific content references",
                        "Highlight recurring commission benefits",
                        "Include calendar link for easy scheduling"
                    ]
                }
            ]
        
        return {
            "score_card": {
                "audience_match_score": audience_match,
                "content_fit_score": content_fit,
                "conversion_potential_score": conversion,
                "overall_score": overall,
                "reasoning": {
                    "audience_match": f"Your {platform} audience shows strong alignment with Submagic's target demographic of content creators and businesses.",
                    "content_fit": "Your content style and posting frequency align well with Submagic's brand messaging.",
                    "conversion": f"With {followers:,} followers and strong engagement, you have high conversion potential for affiliate campaigns."
                }
            },
            "recommendations": recommendations,
            "executive_summary": f"Based on our analysis of @{creator_data.get('username', 'unknown')}'s {platform} profile, we recommend focusing on long-form reviews and tutorial content. This creator's audience (primarily content creators and businesses) represents Submagic's ideal customer base. The recommended materials are tailored to maximize engagement and conversion based on historical performance data."
        }
    
    def _generate_profile_summary(self, creator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the creator's profile"""
        return {
            "username": creator_data.get("username", "Unknown"),
            "platform": creator_data.get("platform", "unknown"),
            "follower_count": creator_data.get("follower_count", creator_data.get("followers", 0)),
            "engagement_estimate": self._estimate_engagement(creator_data),
            "content_themes": self._extract_content_themes(creator_data),
            "audience_overlap_with_submagic": "High" if creator_data.get("follower_count", 0) > 10000 else "Medium"
        }
    
    def _estimate_engagement(self, creator_data: Dict[str, Any]) -> float:
        """Estimate engagement rate based on available data"""
        followers = creator_data.get("follower_count", creator_data.get("followers", 0))
        latest_posts = creator_data.get("latestPosts", creator_data.get("recentVideos", []))
        
        if not latest_posts or followers == 0:
            return 0.0
        
        total_likes = sum(post.get("likes", post.get("likesCount", 0)) for post in latest_posts)
        avg_likes = total_likes / len(latest_posts)
        
        return round((avg_likes / followers) * 100, 2)
    
    def _extract_content_themes(self, creator_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract content themes from posts/captions"""
        latest_posts = creator_data.get("latestPosts", creator_data.get("recentVideos", []))
        
        themes = []
        for post in latest_posts[:5]:
            caption = post.get("caption", post.get("description", ""))
            if caption:
                hashtags = [word for word in caption.split() if word.startswith("#")]
                for tag in hashtags[:3]:
                    themes.append({
                        "theme": tag.replace("#", ""),
                        "source": "hashtag"
                    })
        
        unique_themes = list({t["theme"]: t for t in themes}.values())[:5]
        return unique_themes
    
    async def _get_creator_data(self, creator_id: str) -> Dict[str, Any]:
        """Get creator data by ID (placeholder - connect to database)"""
        return {
            "id": creator_id,
            "username": "sample_creator",
            "platform": "instagram",
            "follower_count": 45000,
            "bio": "Content creator",
            "latestPosts": [
                {"likesCount": 1200, "commentsCount": 45, "caption": "#productivity #growth"},
                {"likesCount": 890, "commentsCount": 32, "caption": "#contentcreation #tips"}
            ]
        }
    
    async def list_reports(self, creator_id: str = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        """List reports with optional filtering"""
        return []
    
    async def get_report(self, report_id: str) -> Dict[str, Any]:
        """Get a report by ID"""
        return {"id": report_id, "status": "not_found"}
    
    def _format_creator_data(self, data: Dict[str, Any]) -> str:
        """Format creator data for prompt"""
        return f"""
Username: @{data.get('username', 'N/A')}
Platform: {data.get('platform', 'N/A')}
Followers: {data.get('follower_count', data.get('followers', 'N/A')):,}
Bio: {data.get('bio', data.get('biography', 'N/A'))}
Engagement Estimate: {self._estimate_engagement(data)}%
"""
    
    def _format_materials(self) -> str:
        """Format affiliate materials for prompt"""
        formatted = []
        for mat in AFFILIATE_MATERIALS:
            formatted.append(f"""
- {mat['name']} ({mat['platform_target']}/{mat['content_type']})
  {mat['description']}
  Best for: {', '.join(mat['best_for_audience_size'])} audiences
  Niches: {', '.join(mat['best_for_niche'][:3])}
""")
        return "\n".join(formatted)
