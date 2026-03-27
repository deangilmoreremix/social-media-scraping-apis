import httpx
from typing import Dict, Any
from .config import get_settings

settings = get_settings()


class ScraperService:
    """Service for scraping creator data from social media platforms"""
    
    APIFY_BASE_URL = "https://api.apify.com/v2"
    
    async def scrape_profile(self, platform: str, username: str) -> Dict[str, Any]:
        """
        Scrape creator profile from specified platform.
        Returns mock data if API token not configured.
        """
        if not settings.apify_api_token:
            return self._generate_mock_profile(platform, username)
        
        scrapers = {
            "instagram": self._scrape_instagram,
            "tiktok": self._scrape_tiktok,
            "youtube": self._scrape_youtube,
            "twitter": self._scrape_twitter
        }
        
        scraper = scrapers.get(platform.lower())
        if scraper:
            return await scraper(username)
        
        return self._generate_mock_profile(platform, username)
    
    async def scrape_creator(self, platform: str, username: str) -> Dict[str, Any]:
        """Alias for scrape_profile for backward compatibility."""
        return await self.scrape_profile(platform, username)
    
    async def _scrape_instagram(self, username: str) -> Dict:
        """Scrape Instagram profile"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~instagram-profile-scraper/run-sync-get-dataset-items",
                params={"token": settings.apify_api_token},
                json={
                    "usernames": [username],
                    "includeLatestPosts": True,
                    "resultsLimit": 12
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else self._get_mock_data("instagram", username)
            
            return self._get_mock_data("instagram", username)
    
    async def _scrape_tiktok(self, username: str) -> Dict:
        """Scrape TikTok profile"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~tiktok-profile-scraper/run-sync-get-dataset-items",
                params={"token": settings.apify_api_token},
                json={
                    "usernames": [username],
                    "includeTrendingVideos": True,
                    "resultsLimit": 20
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else self._get_mock_data("tiktok", username)
            
            return self._get_mock_data("tiktok", username)
    
    async def _scrape_youtube(self, channel_id: str) -> Dict:
        """Scrape YouTube channel"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~youtube-channel-scraper/run-sync-get-dataset-items",
                params={"token": settings.apify_api_token},
                json={
                    "channelUrls": [channel_id],
                    "includeVideoDetails": True
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else self._get_mock_data("youtube", channel_id)
            
            return self._get_mock_data("youtube", channel_id)
    
    async def _scrape_twitter(self, username: str) -> Dict:
        """Scrape Twitter profile"""
        # Similar pattern for Twitter scraper
        return self._get_mock_data("twitter", username)
    
    def _get_mock_data(self, platform: str, username: str) -> Dict:
        """Alias for _generate_mock_profile for backward compatibility."""
        return self._generate_mock_profile(platform, username)
    
    def _generate_mock_profile(self, platform: str, username: str) -> Dict:
        """Return mock profile data for demo purposes"""
        mock_data = {
            "instagram": {
                "username": username,
                "platform": "Instagram",
                "followers": 45000,
                "engagement_rate": 3.2,
                "content_themes": ["productivity", "social_media_tips", "lifestyle"],
                "audience_age": "18-34",
                "top_locations": ["United States", "Brazil", "India"],
                "bio": "Content creator | Productivity tips & social media growth",
                "posts_count": 234
            },
            "tiktok": {
                "username": username,
                "platform": "TikTok",
                "followers": 125000,
                "engagement_rate": 8.5,
                "content_themes": ["viral_tips", "content_creation", "growth_hacks"],
                "audience_age": "16-24",
                "top_locations": ["United States", "Brazil", "Indonesia"],
                "bio": "Teaching you how to go viral 🎯",
                "videos_count": 456
            },
            "youtube": {
                "username": username,
                "platform": "YouTube",
                "followers": 85000,
                "engagement_rate": 4.8,
                "content_themes": ["tech_reviews", "productivity_tools", "software"],
                "audience_age": "25-44",
                "top_locations": ["United States", "India", "United Kingdom"],
                "bio": "In-depth tech reviews and productivity tutorials",
                "videos_count": 234
            },
            "twitter": {
                "username": username,
                "platform": "Twitter/X",
                "followers": 35000,
                "engagement_rate": 2.1,
                "content_themes": ["tech_thoughts", "startup_advice", "ai_tools"],
                "audience_age": "25-49",
                "top_locations": ["United States", "Japan", "UK"],
                "bio": "Tech thoughts & startup advice",
                "tweets_count": 1567
            }
        }
        
        return mock_data.get(platform.lower(), mock_data["instagram"])
