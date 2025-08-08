"""
Vinted API Client with advanced features and error handling
"""

import asyncio
import aiohttp
import logging
import time
import json
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urljoin, urlencode
from dataclasses import dataclass
from datetime import datetime, timedelta

try:
    from .proxy_manager import ProxyManager
    from ..config.settings import settings
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from core.proxy_manager import ProxyManager
    from config.settings import settings

@dataclass
class VintedItem:
    """Vinted item data structure"""
    id: int
    title: str
    price: str
    currency: str
    brand: str
    size: str
    condition: str
    url: str
    photo_url: str
    user_login: str
    created_at: str
    updated_at: str
    location: str = ""
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "currency": self.currency,
            "brand": self.brand,
            "size": self.size,
            "condition": self.condition,
            "url": self.url,
            "photo_url": self.photo_url,
            "user_login": self.user_login,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "location": self.location,
            "description": self.description
        }
        
    @classmethod
    def from_api_data(cls, item_data: Dict[str, Any]) -> "VintedItem":
        """Create VintedItem from API response data"""
        try:
            # Extract photo URL
            photo_url = ""
            if item_data.get("photos") and len(item_data["photos"]) > 0:
                photo_url = item_data["photos"][0].get("high_resolution", {}).get("url", "")
                if not photo_url:
                    photo_url = item_data["photos"][0].get("url", "")
                    
            # Extract user information
            user = item_data.get("user", {})
            user_login = user.get("login", "Unknown")
            
            # Extract brand information
            brand = item_data.get("brand_title", "")
            if not brand and item_data.get("brand"):
                brand = item_data["brand"].get("title", "")
                
            # Extract size information
            size = item_data.get("size_title", "")
            if not size and item_data.get("size"):
                size = item_data["size"].get("title", "")
                
            # Extract condition
            condition = ""
            if item_data.get("status"):
                condition = item_data["status"].get("title", "")
                
            # Build item URL
            item_url = f"https://www.vinted.com/items/{item_data.get('id', '')}"
            
            return cls(
                id=item_data.get("id", 0),
                title=item_data.get("title", ""),
                price=str(item_data.get("price", "")),
                currency=item_data.get("currency", "EUR"),
                brand=brand,
                size=size,
                condition=condition,
                url=item_url,
                photo_url=photo_url,
                user_login=user_login,
                created_at=item_data.get("created_at_ts", ""),
                updated_at=item_data.get("updated_at_ts", ""),
                location=user.get("city", ""),
                description=item_data.get("description", "")
            )
            
        except Exception as e:
            logging.getLogger(__name__).error(f"Error parsing item data: {e}")
            # Return a minimal item with available data
            return cls(
                id=item_data.get("id", 0),
                title=item_data.get("title", "Error parsing item"),
                price="0",
                currency="EUR",
                brand="",
                size="",
                condition="",
                url="",
                photo_url="",
                user_login="",
                created_at="",
                updated_at=""
            )

class RateLimiter:
    """Rate limiter to respect API limits"""
    
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests_per_minute = max_requests_per_minute
        self.requests = []
        
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        # If we're at the limit, wait
        if len(self.requests) >= self.max_requests_per_minute:
            oldest_request = min(self.requests)
            wait_time = 60 - (now - oldest_request)
            if wait_time > 0:
                logging.getLogger(__name__).info(f"Rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                
        # Record this request
        self.requests.append(now)

class VintedAPIClient:
    """Advanced Vinted API client with proxy support"""
    
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.logger = logging.getLogger(__name__)
        self.proxy_manager = proxy_manager
        self.rate_limiter = RateLimiter()
        self.session = None
        
        # API configuration
        self.base_url = settings.vinted_api.base_url
        self.timeout = aiohttp.ClientTimeout(total=settings.vinted_api.timeout)
        
        # Cache for avoiding duplicate requests
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Request statistics
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_session()
        
    async def start_session(self):
        """Start aiohttp session"""
        if not self.session:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=10,
                keepalive_timeout=30
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                }
            )
            
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    def _get_cache_key(self, url: str, params: Dict = None) -> str:
        """Generate cache key for request"""
        cache_data = f"{url}_{params}" if params else url
        return hashlib.md5(cache_data.encode()).hexdigest()
        
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
            
        cached_time = self.cache[cache_key].get("timestamp", 0)
        return time.time() - cached_time < self.cache_ttl
        
    async def _make_request(
        self, 
        url: str, 
        params: Optional[Dict] = None,
        use_cache: bool = True,
        max_retries: int = 3
    ) -> Optional[Dict]:
        """
        Make HTTP request with retry logic and proxy support
        """
        if not self.session:
            await self.start_session()
            
        # Check cache first
        cache_key = self._get_cache_key(url, params)
        if use_cache and self._is_cache_valid(cache_key):
            self.logger.debug(f"Cache hit for {url}")
            return self.cache[cache_key]["data"]
            
        # Rate limiting
        await self.rate_limiter.wait_if_needed()
        
        last_exception = None
        
        for attempt in range(max_retries):
            proxy_url = None
            proxy_config = None
            
            # Get proxy if manager is available
            if self.proxy_manager:
                try:
                    proxy_result = await self.proxy_manager.get_proxy_for_request("round_robin")
                    if proxy_result:
                        proxy_url, proxy_config = proxy_result
                except Exception as e:
                    self.logger.warning(f"Error getting proxy: {e}")
                    
            try:
                start_time = time.time()
                
                kwargs = {}
                if proxy_config:
                    kwargs["proxy"] = proxy_url
                    
                self.logger.debug(f"Making request to {url} (attempt {attempt + 1}/{max_retries})")
                
                async with self.session.get(url, params=params, **kwargs) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Record success
                        self.request_count += 1
                        self.success_count += 1
                        
                        if proxy_url and self.proxy_manager:
                            self.proxy_manager.record_request_result(proxy_url, True, response_time)
                            
                        # Cache the response
                        if use_cache:
                            self.cache[cache_key] = {
                                "data": data,
                                "timestamp": time.time()
                            }
                            
                        return data
                        
                    elif response.status == 429:  # Rate limited
                        self.logger.warning(f"Rate limited (429), waiting before retry...")
                        await asyncio.sleep(min(60, 2 ** attempt))
                        continue
                        
                    elif response.status in [403, 404]:  # Client errors
                        self.logger.error(f"Client error {response.status} for {url}")
                        break
                        
                    else:
                        self.logger.warning(f"HTTP {response.status} for {url}")
                        
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout for {url} (attempt {attempt + 1})")
                last_exception = "Timeout"
                
            except Exception as e:
                self.logger.warning(f"Request error for {url}: {e}")
                last_exception = str(e)
                
            # Record failure
            self.request_count += 1
            self.error_count += 1
            
            if proxy_url and self.proxy_manager:
                self.proxy_manager.record_request_result(proxy_url, False)
                
            # Wait before retry
            if attempt < max_retries - 1:
                wait_time = min(10, 2 ** attempt)
                await asyncio.sleep(wait_time)
                
        self.logger.error(f"All retry attempts failed for {url}. Last error: {last_exception}")
        return None
        
    async def search_items(
        self,
        search_query: str = "",
        price_from: Optional[int] = None,
        price_to: Optional[int] = None,
        brand_ids: Optional[List[int]] = None,
        size_ids: Optional[List[int]] = None,
        material_ids: Optional[List[int]] = None,
        color_ids: Optional[List[int]] = None,
        status_ids: Optional[List[int]] = None,
        country_code: str = "FR",
        currency: str = "EUR",
        order: str = "newest_first",
        per_page: int = 20,
        page: int = 1
    ) -> List[VintedItem]:
        """
        Search for items on Vinted
        
        Args:
            search_query: Search text
            price_from: Minimum price
            price_to: Maximum price
            brand_ids: List of brand IDs
            size_ids: List of size IDs
            material_ids: List of material IDs
            color_ids: List of color IDs
            status_ids: List of status IDs (1=New with tags, 2=Very good, etc.)
            country_code: Country code
            currency: Currency code
            order: Sort order (newest_first, price_low_to_high, price_high_to_low, relevance)
            per_page: Items per page (max 96)
            page: Page number
            
        Returns:
            List of VintedItem objects
        """
        
        # Build search parameters
        params = {
            "order": order,
            "currency": currency,
            "per_page": min(per_page, 96),  # API limit
            "page": page
        }
        
        # Add search query
        if search_query:
            params["search_text"] = search_query
            
        # Add price filters
        if price_from is not None:
            params["price_from"] = price_from
        if price_to is not None:
            params["price_to"] = price_to
            
        # Add filters
        if brand_ids:
            params["brand_ids[]"] = brand_ids
        if size_ids:
            params["size_ids[]"] = size_ids
        if material_ids:
            params["material_ids[]"] = material_ids
        if color_ids:
            params["color_ids[]"] = color_ids
        if status_ids:
            params["status_ids[]"] = status_ids
            
        # Build URL
        url = urljoin(self.base_url, "/api/v2/catalog/items")
        
        self.logger.debug(f"Searching items with params: {params}")
        
        try:
            data = await self._make_request(url, params)
            if not data:
                return []
                
            items = data.get("items", [])
            vinted_items = []
            
            for item_data in items:
                try:
                    vinted_item = VintedItem.from_api_data(item_data)
                    vinted_items.append(vinted_item)
                except Exception as e:
                    self.logger.error(f"Error parsing item: {e}")
                    continue
                    
            self.logger.info(f"Found {len(vinted_items)} items")
            return vinted_items
            
        except Exception as e:
            self.logger.error(f"Error searching items: {e}")
            return []
            
    async def get_item_by_id(self, item_id: int) -> Optional[VintedItem]:
        """Get detailed information about a specific item"""
        url = urljoin(self.base_url, f"/api/v2/items/{item_id}")
        
        try:
            data = await self._make_request(url)
            if not data:
                return None
                
            item_data = data.get("item")
            if not item_data:
                return None
                
            return VintedItem.from_api_data(item_data)
            
        except Exception as e:
            self.logger.error(f"Error getting item {item_id}: {e}")
            return None
            
    async def get_latest_items(
        self,
        search_url: str,
        max_items: int = 10
    ) -> List[VintedItem]:
        """
        Get latest items from a Vinted search URL
        
        Args:
            search_url: Full Vinted search URL
            max_items: Maximum number of items to return
            
        Returns:
            List of latest VintedItem objects
        """
        try:
            # Extract search parameters from URL
            from urllib.parse import urlparse, parse_qs
            
            parsed_url = urlparse(search_url)
            query_params = parse_qs(parsed_url.query)
            
            # Convert query parameters to API parameters
            api_params = {}
            
            # Map common parameters
            param_mapping = {
                "search_text": "search_text",
                "price_from": "price_from",
                "price_to": "price_to",
                "brand_ids[]": "brand_ids",
                "size_ids[]": "size_ids",
                "color_ids[]": "color_ids",
                "status_ids[]": "status_ids",
                "currency": "currency"
            }
            
            for url_param, api_param in param_mapping.items():
                if url_param in query_params:
                    values = query_params[url_param]
                    if len(values) == 1:
                        # Single value
                        value = values[0]
                        if api_param in ["price_from", "price_to"]:
                            try:
                                api_params[api_param] = int(value)
                            except ValueError:
                                pass
                        elif api_param.endswith("_ids"):
                            try:
                                api_params[api_param] = [int(value)]
                            except ValueError:
                                pass
                        else:
                            api_params[api_param] = value
                    else:
                        # Multiple values (for arrays)
                        if api_param.endswith("_ids"):
                            try:
                                api_params[api_param] = [int(v) for v in values]
                            except ValueError:
                                pass
                                
            # Always sort by newest first
            api_params["order"] = "newest_first"
            api_params["per_page"] = min(max_items, 96)
            
            self.logger.debug(f"Extracted API params: {api_params}")
            
            # Make the search
            items = await self.search_items(**api_params)
            
            return items[:max_items]
            
        except Exception as e:
            self.logger.error(f"Error getting latest items from URL {search_url}: {e}")
            return []
            
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics"""
        success_rate = (
            self.success_count / self.request_count 
            if self.request_count > 0 else 0
        )
        
        stats = {
            "total_requests": self.request_count,
            "successful_requests": self.success_count,
            "failed_requests": self.error_count,
            "success_rate": success_rate,
            "cache_entries": len(self.cache)
        }
        
        if self.proxy_manager:
            proxy_stats = self.proxy_manager.get_stats()
            stats["proxy_stats"] = proxy_stats
            
        return stats
