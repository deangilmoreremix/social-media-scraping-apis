import httpx
from typing import Dict, Any, Optional
from ..config import get_settings

settings = get_settings()


class ApifyService:
    APIFY_BASE_URL = "https://api.apify.com/v2"
    
    def __init__(self):
        self.api_token = settings.apify_api_token
    
    async def scrape_instagram_profile(self, username: str) -> Dict[str, Any]:
        """Scrape Instagram profile using Apify Instagram Profile Scraper"""
        if not self.api_token:
            return self._mock_instagram_data(username)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~instagram-profile-scraper/run-sync-get-dataset-items",
                params={"token": self.api_token},
                json={
                    "usernames": [username],
                    "includeLatestPosts": True,
                    "resultsLimit": 12
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else {}
            else:
                return self._mock_instagram_data(username)
    
    async def scrape_tiktok_profile(self, username: str) -> Dict[str, Any]:
        """Scrape TikTok profile using Apify TikTok Profile Scraper"""
        if not self.api_token:
            return self._mock_tiktok_data(username)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~tiktok-profile-scraper/run-sync-get-dataset-items",
                params={"token": self.api_token},
                json={
                    "usernames": [username],
                    "includeTrendingVideos": True,
                    "resultsLimit": 20
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else {}
            else:
                return self._mock_tiktok_data(username)
    
    async def scrape_youtube_channel(self, channel_id: str) -> Dict[str, Any]:
        """Scrape YouTube channel using Apify YouTube Channel Scraper"""
        if not self.api_token:
            return self._mock_youtube_data(channel_id)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.APIFY_BASE_URL}/acts/apidojo~youtube-channel-scraper/run-sync-get-dataset-items",
                params={"token": self.api_token},
                json={
                    "channelUrls": [channel_id],
                    "includeVideoDetails": True
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else {}
            else:
                return self._mock_youtube_data(channel_id)
    
    def _mock_instagram_data(self, username: str) -> Dict[str, Any]:
        """Mock data for development/testing"""
        return {
            "username": username,
            "displayName": f"@{username}",
            "biography": f"Content creator sharing tips about productivity and social media growth",
            "followersCount": 45000,
            "followingCount": 1200,
            "postsCount": 234,
            "profilePictureUrl": f"https://i.instagram.com/{username}/profile.jpg",
            "isVerified": False,
            "latestPosts": [
                {
                    "type": "Video",
                    "likesCount": 1200,
                    "commentsCount": 45,
                    "caption": "Pro tip for growing your audience #growth #socialmedia"
                },
                {
                    "type": "Image",
                    "likesCount": 890,
                    "commentsCount": 32,
                    "caption": "My morning routine for maximum productivity"
                }
            ],
            "scrapedAt": "2026-03-27T10:00:00Z",
            "source": "mock"
        }
    
    def _mock_tiktok_data(self, username: str) -> Dict[str, Any]:
        """Mock TikTok data for development/testing"""
        return {
            "username": username,
            "displayName": f"@{username}",
            "bio": "Creating viral content tips | 100K+ followers",
            "followers": 125000,
            "following": 890,
            "likes": 2100000,
            "videos": 456,
            "profilePicture": f"https://tiktok.com/{username}/avatar.jpg",
            "isVerified": False,
            "recentVideos": [
                {
                    "likes": 15000,
                    "comments": 340,
                    "shares": 890,
                    "description": "POV: You finally find the perfect editing app #fyp #viral"
                },
                {
                    "likes": 22000,
                    "comments": 560,
                    "shares": 1200,
                    "description": "This one hack changed my content forever"
                }
            ],
            "scrapedAt": "2026-03-27T10:00:00Z",
            "source": "mock"
        }
    
    def _mock_youtube_data(self, channel_id: str) -> Dict[str, Any]:
        """Mock YouTube data for development/testing"""
        return {
            "channelId": channel_id,
            "title": f"Channel {channel_id}",
            "description": "Tech reviews, productivity tips, and behind-the-scenes content",
            "subscribers": 85000,
            "videos": 234,
            "totalViews": 5200000,
            "profilePicture": f"https://yt3.ggpht.com/{channel_id}",
            "isVerified": False,
            "recentVideos": [
                {
                    "title": "My ENTIRE Editing Workflow (2026)",
                    "views": 45000,
                    "likes": 3200,
                    "comments": 189,
                    "duration": "12:34"
                },
                {
                    "title": "Why I Switched to AI Editing Tools",
                    "views": 67000,
                    "likes": 5100,
                    "comments": 340,
                    "duration": "15:22"
                }
            ],
            "scrapedAt": "2026-03-27T10:00:00Z",
            "source": "mock"
        }
