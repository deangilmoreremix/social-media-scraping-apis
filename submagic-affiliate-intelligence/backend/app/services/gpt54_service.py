from openai import OpenAI
from typing import Generator, Dict, Any
import json
import time
from .config import get_settings

settings = get_settings()


class GPT54Service:
    """GPT-5.4 service for affiliate intelligence analysis"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.materials_library = self._get_materials_library()
    
    def _get_materials_library(self) -> str:
        """Return the affiliate materials library"""
        return """
AFFILIATE MATERIALS:

1. YOUTUBE_LONG_FORM - "Submagic Review Script - Long Form"
   - Comprehensive review script for YouTube videos (5-10 minutes)
   - Best for: Tech reviewers, productivity creators, content creators
   - Include: Before/after demos, time saved metrics, price point discussion

2. TIKTOK_DEMO - "TikTok Demo Hook"
   - 15-30 second hook video showcasing Submagic's AI captions
   - Best for: Micro/small creators, social media influencers
   - Include: Quick transformation, trending sounds, clear CTA

3. INSTAGRAM_REELS - "Instagram Reels Tutorial"
   - Step-by-step tutorial for creating engaging Reels with Submagic
   - Best for: Lifestyle creators, small businesses, educators
   - Include: Clear UI demos, swipe-up pattern, trending audio

4. EMAIL_TEMPLATE - "Email Outreach Template"
   - Professional template for affiliate/partnership outreach
   - Best for: Coaches, consultants, B2B influencers
   - Include: Personalized intro, recurring commission highlight, easy CTA

5. COMPARISON_POST - "Comparison Post Template"
   - Submagic vs competitors comparison content
   - Best for: Tech reviewers, thorough analysts
   - Include: Honest pros/cons, unique features, clear verdict

6. SUCCESS_STORY - "Success Story Template"
   - Personal transformation story with Submagic
   - Best for: Long-form bloggers, case study creators
   - Include: Specific metrics, personal journey, embedded demo
"""
    
    def analyze_stream(self, platform: str, username: str, tone: str = "professional") -> Dict:
        """
        Analyze a creator and return streaming-ready data.
        """
        # Mock data for demo (replace with actual scraping + GPT-5.4)
        return self._generate_mock_analysis(platform, username, tone)
    
    def _generate_mock_analysis(self, platform: str, username: str, tone: str) -> Dict:
        """Generate mock analysis based on platform and tone"""
        
        # Mock creator data based on platform
        creator_data = {
            "instagram": {
                "username": username,
                "platform": "Instagram",
                "followers": 45000,
                "engagement_rate": 3.2,
                "content_themes": ["productivity", "social_media_tips", "lifestyle"],
                "audience_age": "18-34",
                "top_locations": ["United States", "Brazil", "India"],
                "content_style": "Educational lifestyle content with reels tutorials"
            },
            "tiktok": {
                "username": username,
                "platform": "TikTok",
                "followers": 125000,
                "engagement_rate": 8.5,
                "content_themes": ["viral_tips", "content_creation", "growth_hacks"],
                "audience_age": "16-24",
                "top_locations": ["United States", "Brazil", "Indonesia"],
                "content_style": "Fast-paced, trend-driven short-form content"
            },
            "youtube": {
                "username": username,
                "platform": "YouTube",
                "followers": 85000,
                "engagement_rate": 4.8,
                "content_themes": ["tech_reviews", "productivity_tools", "software"],
                "audience_age": "25-44",
                "top_locations": ["United States", "India", "United Kingdom"],
                "content_style": "In-depth reviews and detailed tutorials"
            },
            "twitter": {
                "username": username,
                "platform": "Twitter/X",
                "followers": 35000,
                "engagement_rate": 2.1,
                "content_themes": ["tech_thoughts", "startup_advice", "ai_tools"],
                "audience_age": "25-49",
                "top_locations": ["United States", "Japan", "UK"],
                "content_style": "Concise thoughts, threads, and industry insights"
            }
        }
        
        # Tone adjustments
        tone_styles = {
            "professional": "Business-focused, emphasize ROI and efficiency",
            "casual": "Fun and relatable, emphasize creativity and fun",
            "educational": "Detailed explanations, emphasize learning value",
            "direct": "Straight to the point, emphasize quick results"
        }
        
        creator = creator_data.get(platform, creator_data["instagram"])
        
        return {
            "creator": creator,
            "analysis": {
                "audience_match": self._calculate_audience_match(creator),
                "content_fit": self._calculate_content_fit(creator),
                "conversion_potential": self._calculate_conversion_potential(creator),
                "recommended_materials": self._get_recommendations(creator, tone),
                "engagement_tips": self._get_engagement_tips(creator, tone)
            }
        }
    
    def _calculate_audience_match(self, creator: Dict) -> int:
        """Calculate audience match score (0-100)"""
        # Higher engagement + younger audience = better match for Submagic
        base_score = 70
        if creator["engagement_rate"] > 5:
            base_score += 15
        if creator["audience_age"] in ["16-24", "18-34"]:
            base_score += 15
        return min(100, base_score)
    
    def _calculate_content_fit(self, creator: Dict) -> int:
        """Calculate content fit score (0-100)"""
        # Content creators, tech, productivity = great fit
        themes = creator["content_themes"]
        fit_indicators = ["productivity", "tech", "content_creation", "social_media", "software"]
        matches = sum(1 for t in themes if any(ind in t for ind in fit_indicators))
        return min(100, 50 + (matches * 15))
    
    def _calculate_conversion_potential(self, creator: Dict) -> int:
        """Calculate conversion potential score (0-100)"""
        followers = creator["followers"]
        engagement = creator["engagement_rate"]
        
        # Balance between reach and engagement
        reach_score = min(40, followers / 1000)
        engagement_score = min(60, engagement * 5)
        return int(reach_score + engagement_score)
    
    def _get_recommendations(self, creator: Dict, tone: str) -> list:
        """Get recommended materials for this creator"""
        platform = creator["platform"].lower()
        
        recommendations = {
            "instagram": [
                {
                    "material": "Instagram Reels Tutorial",
                    "score": 92,
                    "reasoning": "Your reels-focused content style aligns perfectly with Submagic's tutorial format.",
                    "posting_times": ["9 AM EST", "12 PM EST", "7 PM EST"],
                    "tips": ["Use clear UI demonstrations", "Add trending audio", "Include before/after transformations"]
                },
                {
                    "material": "TikTok Demo Hook",
                    "score": 88,
                    "reasoning": "Quick demo format ideal for your short-form expertise.",
                    "posting_times": ["6 PM EST", "9 PM EST"],
                    "tips": ["Hook viewers in first 2 seconds", "Show transformation clearly", "Use text overlays"]
                }
            ],
            "tiktok": [
                {
                    "material": "TikTok Demo Hook",
                    "score": 95,
                    "reasoning": "Your viral content style is perfect for this quick demo format.",
                    "posting_times": ["7 PM EST", "9 PM EST", "11 PM EST"],
                    "tips": ["Use trending sounds", "Show instant results", "Include clear CTA"]
                },
                {
                    "material": "Instagram Reels Tutorial",
                    "score": 82,
                    "reasoning": "Tutorial content performs well on your audience.",
                    "posting_times": ["12 PM EST", "6 PM EST"],
                    "tips": ["Step-by-step format", "Trending audio in background", "Clear call-to-action"]
                }
            ],
            "youtube": [
                {
                    "material": "YouTube Long Form Review",
                    "score": 94,
                    "reasoning": "Your in-depth review style is perfect for comprehensive Submagic coverage.",
                    "posting_times": ["2 PM EST", "10 AM EST"],
                    "tips": ["Include real before/after examples", "Mention specific time savings", "Address price point directly"]
                },
                {
                    "material": "Comparison Post Template",
                    "score": 87,
                    "reasoning": "Your analytical content style makes comparison videos highly effective.",
                    "posting_times": ["11 AM EST", "4 PM EST"],
                    "tips": ["Be honest about pros and cons", "Use timestamps", "Include clear verdict"]
                }
            ],
            "twitter": [
                {
                    "material": "Email Outreach Template",
                    "score": 85,
                    "reasoning": "Direct outreach is effective for professional networking.",
                    "posting_times": ["Tuesday 10 AM EST", "Thursday 2 PM EST"],
                    "tips": ["Personalize with content references", "Highlight recurring commission", "Include calendar link"]
                },
                {
                    "material": "Success Story Template",
                    "score": 78,
                    "reasoning": "Thread-format storytelling works well for your audience.",
                    "posting_times": ["Wednesday 11 AM EST"],
                    "tips": ["Use specific metrics", "Personal journey format", "Include embedded examples"]
                }
            ]
        }
        
        return recommendations.get(platform, recommendations["instagram"])
    
    def _get_engagement_tips(self, creator: Dict, tone: str) -> list:
        """Get engagement tips for this creator"""
        return [
            f"Focus on {creator['content_themes'][0].replace('_', ' ')} content to maximize resonance",
            f"Your {creator['audience_age']} audience responds well to authentic demonstrations",
            f"Use Submagic's before/after feature to show immediate value",
            f"Target {creator['top_locations'][0]} audience with localized content"
        ]
    
    async def analyze_with_ai(self, profile_data: Dict, tone: str) -> Dict:
        """Analyze creator using GPT-5.4 AI."""
        if not self.client:
            return self._generate_mock_analysis(
                profile_data.get("platform", "instagram").lower(),
                profile_data.get("username", ""),
                tone
            )
        
        prompt = f"""
        Analyze this social media creator for Submagic affiliate partnership potential.
        
        Creator Data:
        - Platform: {profile_data.get('platform', 'N/A')}
        - Username: {profile_data.get('username', 'N/A')}
        - Followers: {profile_data.get('followers', 0):,}
        - Engagement Rate: {profile_data.get('engagement_rate', 0)}%
        - Content Themes: {', '.join(profile_data.get('content_themes', []))}
        - Audience Age: {profile_data.get('audience_age', 'N/A')}
        - Top Locations: {', '.join(profile_data.get('top_locations', []))}
        
        Analyze and return JSON with:
        1. audience_match (0-100 score)
        2. content_fit (0-100 score)  
        3. conversion_potential (0-100 score)
        4. reasoning (brief explanation)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                reasoning={"effort": "medium"},
                messages=[
                    {"role": "system", "content": "You are an affiliate marketing analyst. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return self._generate_mock_analysis(
                profile_data.get("platform", "instagram").lower(),
                profile_data.get("username", ""),
                tone
            )
    
    def _generate_strategy(self, profile_data: Dict, analysis_result: Dict, materials: list) -> Dict:
        """Generate campaign strategy."""
        creator = profile_data
        analysis = analysis_result if isinstance(analysis_result, dict) else {"audience_match": 75, "content_fit": 75, "conversion_potential": 75}
        
        return {
            "next_steps": [
                f"Reach out to @{creator.get('username', '')} with personalized pitch",
                f"Provide free Submagic access for testing",
                f"Share {materials[0].get('material', 'recommended material') if materials else 'recommended materials'} template",
                "Schedule follow-up after 1 week to discuss results"
            ],
            "success_metrics": {
                "target_engagement": "4%+ on affiliate posts",
                "target_ctr": "2-3% on affiliate links",
                "target_conversion": f"{(analysis.get('conversion_potential', 75) / 100 * 5):.1f}%"
            },
            "commission_structure": {
                "base_rate": "30% recurring (lifetime)",
                "bonus_tiers": "Quarterly performance bonuses",
                "high_performer_threshold": "50+ conversions/month"
            }
        }
    
    async def generate_report(self, creator_url: str, analysis_data: Dict) -> str:
        """Generate comprehensive report using GPT-5.4"""
        if not self.client:
            return self._generate_mock_report(creator_url, analysis_data)
        
        prompt = f"""
        Create a comprehensive affiliate intelligence report for this creator:
        
        Creator URL: {creator_url}
        Platform: {analysis_data['creator']['platform']}
        Username: {analysis_data['creator']['username']}
        Followers: {analysis_data['creator']['followers']:,}
        Engagement Rate: {analysis_data['creator']['engagement_rate']}%
        
        Analysis:
        - Audience Match Score: {analysis_data['analysis']['audience_match']}/100
        - Content Fit Score: {analysis_data['analysis']['content_fit']}/100
        - Conversion Potential: {analysis_data['analysis']['conversion_potential']}/100
        
        Recommended Materials:
        {json.dumps(analysis_data['analysis']['recommended_materials'], indent=2)}
        
        Format the report in markdown with sections for:
        1. Executive Summary
        2. Creator Profile
        3. Campaign Score Card
        4. Material Recommendations
        5. Engagement Strategy
        """
        
        response = self.client.chat.completions.create(
            model="gpt-5.4",
            reasoning={"effort": "high"},
            messages=[
                {"role": "system", "content": "You are an expert affiliate marketing strategist for Submagic, the AI video editing platform."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    def _generate_mock_report(self, creator_url: str, analysis_data: Dict) -> str:
        """Generate mock report for demo"""
        creator = analysis_data['creator']
        analysis = analysis_data['analysis']
        
        report = f"""
# Submagic Affiliate Intelligence Report

## Executive Summary

Analysis of @{creator['username']} on {creator['platform']} reveals strong potential 
for Submagic affiliate partnership. With {creator['followers']:,} followers and a 
{creator['engagement_rate']}% engagement rate, this creator demonstrates excellent 
qualities for promoting AI-powered video editing tools.

## Campaign Score Card

| Metric | Score | Assessment |
|--------|-------|------------|
| Audience Match | {analysis['audience_match']}/100 | {'Excellent' if analysis['audience_match'] >= 80 else 'Good' if analysis['audience_match'] >= 60 else 'Fair'} |
| Content Fit | {analysis['content_fit']}/100 | {'Excellent' if analysis['content_fit'] >= 80 else 'Good' if analysis['content_fit'] >= 60 else 'Fair'} |
| Conversion Potential | {analysis['conversion_potential']}/100 | {'Excellent' if analysis['conversion_potential'] >= 80 else 'Good' if analysis['conversion_potential'] >= 60 else 'Fair'} |

## Recommended Materials

"""
        
        for i, rec in enumerate(analysis['recommended_materials'], 1):
            report += f"""
### {i}. {rec['material']} (Match Score: {rec['score']}%)
{rec['reasoning']}

**Best Posting Times:**
{', '.join(rec['posting_times'])}

**Engagement Tips:**
"""
            for tip in rec['tips']:
                report += f"- {tip}\n"
        
        report += """
## Next Steps

1. Reach out to creator with personalized pitch
2. Provide free Submagic access for testing
3. Share recommended materials and best practices
4. Schedule follow-up to discuss performance
"""
        
        return report
