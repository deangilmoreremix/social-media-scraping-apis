from typing import Dict, Any, List, Optional
from datetime import datetime
import csv
import io
import re
from .apify_service import ApifyService

apify_service = ApifyService()


class CreatorAnalysisService:
    """Service for analyzing creator profiles"""
    
    def __init__(self):
        self.creators_db: Dict[str, Dict] = {}
    
    async def analyze_profile(self, profile_url: str) -> Dict[str, Any]:
        """Analyze a single creator profile from URL"""
        platform = self._detect_platform(profile_url)
        username = self._extract_username(profile_url, platform)
        
        if not platform or not username:
            return {
                "success": False,
                "error": "Could not detect platform or username from URL"
            }
        
        if platform == "instagram":
            scraped_data = await apify_service.scrape_instagram_profile(username)
        elif platform == "tiktok":
            scraped_data = await apify_service.scrape_tiktok_profile(username)
        elif platform == "youtube":
            scraped_data = await apify_service.scrape_youtube_channel(username)
        else:
            scraped_data = self._generate_generic_data(username, platform)
        
        creator_data = self._process_scraped_data(scraped_data, platform, username, profile_url)
        
        creator_id = creator_data["id"]
        self.creators_db[creator_id] = creator_data
        
        return {
            "success": True,
            "creator": creator_data
        }
    
    async def bulk_analyze(self, csv_content: str) -> Dict[str, Any]:
        """Analyze multiple creators from CSV content"""
        results = {
            "success": [],
            "failed": [],
            "total": 0
        }
        
        reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(reader)
        results["total"] = len(rows)
        
        for row in rows:
            url = row.get("url", row.get("profile_url", ""))
            if url:
                result = await self.analyze_profile(url)
                if result.get("success"):
                    results["success"].append(result["creator"]["id"])
                else:
                    results["failed"].append({
                        "url": url,
                        "error": result.get("error")
                    })
        
        return results
    
    async def get_creator(self, creator_id: str) -> Optional[Dict[str, Any]]:
        """Get a creator by ID"""
        return self.creators_db.get(creator_id)
    
    async def list_creators(
        self,
        platform: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List all creators with optional filtering"""
        creators = list(self.creators_db.values())
        
        if platform:
            creators = [c for c in creators if c.get("platform") == platform]
        
        return creators[offset:offset + limit]
    
    def _detect_platform(self, url: str) -> Optional[str]:
        """Detect social media platform from URL"""
        url_lower = url.lower()
        
        if "instagram.com" in url_lower or "ig @" in url_lower:
            return "instagram"
        elif "tiktok.com" in url_lower:
            return "tiktok"
        elif "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "youtube"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "twitter"
        
        return None
    
    def _extract_username(self, url: str, platform: str) -> Optional[str]:
        """Extract username from profile URL"""
        patterns = {
            "instagram": r"(?:instagram\.com/|@)([a-zA-Z0-9._]+)",
            "tiktok": r"(?:tiktok\.com/@)([a-zA-Z0-9._]+)",
            "youtube": r"(?:youtube\.com/|@)([a-zA-Z0-9_-]+)",
            "twitter": r"(?:twitter\.com/|x\.com/@)([a-zA-Z0-9_]+)"
        }
        
        pattern = patterns.get(platform)
        if pattern:
            match = re.search(pattern, url)
            if match:
                return match.group(1).rstrip("/")
        
        return None
    
    def _process_scraped_data(
        self,
        scraped_data: Dict[str, Any],
        platform: str,
        username: str,
        profile_url: str
    ) -> Dict[str, Any]:
        """Process scraped data into standardized format"""
        
        followers = (
            scraped_data.get("followersCount") or
            scraped_data.get("followers") or
            scraped_data.get("subscribers") or
            0
        )
        
        latest_posts = scraped_data.get("latestPosts", scraped_data.get("recentVideos", []))
        engagement_rate = self._calculate_engagement_rate(latest_posts, followers)
        
        return {
            "id": f"{platform}_{username}_{datetime.now().timestamp()}",
            "platform": platform,
            "username": username,
            "profile_url": profile_url,
            "display_name": scraped_data.get("displayName") or scraped_data.get("title", f"@{username}"),
            "bio": scraped_data.get("biography") or scraped_data.get("bio") or scraped_data.get("description", ""),
            "follower_count": followers,
            "following_count": scraped_data.get("followingCount") or scraped_data.get("following") or 0,
            "engagement_rate": engagement_rate,
            "total_posts": scraped_data.get("postsCount") or scraped_data.get("videos") or len(latest_posts),
            "content_themes": self._extract_content_themes(latest_posts),
            "audience_demographics": self._estimate_demographics(platform, followers),
            "profile_image_url": scraped_data.get("profilePictureUrl") or scraped_data.get("profilePicture", ""),
            "is_verified": scraped_data.get("isVerified", False),
            "scraped_data": {
                "raw_data": scraped_data,
                "scraped_at": datetime.now().isoformat(),
                "source_actor": scraped_data.get("source", "unknown")
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def _calculate_engagement_rate(self, posts: List[Dict], followers: int) -> float:
        """Calculate engagement rate from posts and followers"""
        if not posts or followers == 0:
            return 0.0
        
        total_engagement = 0
        for post in posts:
            likes = post.get("likes", post.get("likesCount", 0))
            comments = post.get("comments", post.get("commentsCount", 0))
            total_engagement += likes + (comments * 2)
        
        avg_engagement = total_engagement / len(posts)
        return round((avg_engagement / followers) * 100, 2)
    
    def _extract_content_themes(self, posts: List[Dict]) -> List[Dict[str, Any]]:
        """Extract content themes from posts"""
        theme_counts = {}
        
        for post in posts:
            text = post.get("caption", "") or post.get("description", "") or post.get("title", "")
            
            hashtags = re.findall(r'#(\w+)', text)
            for tag in hashtags:
                theme = tag.lower()
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        themes = [
            {"theme": t, "count": c, "percentage": round((c / len(posts)) * 100, 1)}
            for t, c in sorted(theme_counts.items(), key=lambda x: -x[1])[:10]
        ]
        
        return themes
    
    def _estimate_demographics(self, platform: str, followers: int) -> Dict[str, Any]:
        """Estimate audience demographics based on platform and size"""
        
        if followers > 100000:
            size_category = "large"
        elif followers > 10000:
            size_category = "medium"
        elif followers > 1000:
            size_category = "small"
        else:
            size_category = "micro"
        
        platform_demographics = {
            "instagram": {
                "primary_age": "18-34",
                "top_locations": ["United States", "Brazil", "India", "United Kingdom"],
                "gender_split": {"female": 60, "male": 38, "other": 2}
            },
            "tiktok": {
                "primary_age": "16-24",
                "top_locations": ["United States", "Brazil", "Indonesia", "Mexico"],
                "gender_split": {"female": 55, "male": 43, "other": 2}
            },
            "youtube": {
                "primary_age": "25-44",
                "top_locations": ["United States", "India", "United Kingdom", "Brazil"],
                "gender_split": {"male": 55, "female": 43, "other": 2}
            },
            "twitter": {
                "primary_age": "25-49",
                "top_locations": ["United States", "Japan", "United Kingdom", "India"],
                "gender_split": {"male": 65, "female": 33, "other": 2}
            }
        }
        
        demographics = platform_demographics.get(platform, platform_demographics["instagram"])
        demographics["size_category"] = size_category
        
        return demographics
    
    def _generate_generic_data(self, username: str, platform: str) -> Dict[str, Any]:
        """Generate mock data for unknown platforms"""
        return {
            "username": username,
            "displayName": f"@{username}",
            "bio": "Social media content creator",
            "followersCount": 10000,
            "followingCount": 500,
            "postsCount": 100,
            "isVerified": False,
            "latestPosts": [],
            "scrapedAt": datetime.now().isoformat(),
            "source": "generic"
        }
