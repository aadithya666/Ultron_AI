"""
API Handler for external integrations
Manages requests to external APIs
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime

class APIHandler:
    """Handles external API calls"""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
        
    def fetch_weather(self, location: str = None, units: str = "metric") -> Optional[Dict]:
        """
        Fetch weather data from OpenWeather API
        
        Args:
            location: Location name or coordinates
            units: metric, imperial, standard
            
        Returns:
            Weather data or None
        """
        try:
            location = location or self.config.DEFAULT_LOCATION
            api_key = self.config.OPENWEATHER_API_KEY
            
            if api_key == 'your_api_key_here':
                return {"error": "OpenWeather API key not configured"}
            
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": api_key,
                "units": units
            }
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def fetch_news(self, query: str = None, country: str = None) -> Optional[Dict]:
        """
        Fetch news from NewsAPI
        
        Args:
            query: Search query
            country: Country code
            
        Returns:
            News data or None
        """
        try:
            api_key = self.config.NEWS_API_KEY
            
            if api_key == 'your_api_key_here':
                return {"error": "NewsAPI key not configured"}
            
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": api_key,
                "pageSize": 5
            }
            
            if query:
                params["q"] = query
            
            if country:
                params["country"] = country
            else:
                params["country"] = self.config.DEFAULT_COUNTRY_CODE
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"News API error: {e}")
            return None
    
    def search_wikipedia(self, query: str, auto_suggest: bool = True) -> Optional[Dict]:
        """
        Search Wikipedia for information
        
        Args:
            query: Search query
            auto_suggest: Auto-suggest similar queries
            
        Returns:
            Wikipedia data or None
        """
        try:
            import wikipedia
            
            result = wikipedia.summary(query, auto_suggest=auto_suggest, sentences=3)
            return {
                "title": query,
                "summary": result,
                "source": "wikipedia"
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            return {"error": f"Ambiguous: {e.options[:5]}"}
        except wikipedia.exceptions.PageError:
            return {"error": f"No Wikipedia page found for '{query}'"}
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return None
    
    def fetch_data(self, url: str, params: Dict = None, headers: Dict = None) -> Optional[Dict]:
        """
        Generic GET request to fetch data
        
        Args:
            url: API endpoint URL
            params: Query parameters
            headers: Request headers
            
        Returns:
            Response JSON or None
        """
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"API fetch error: {e}")
            return None
    
    def post_data(self, url: str, data: Dict = None, headers: Dict = None) -> Optional[Dict]:
        """
        Generic POST request
        
        Args:
            url: API endpoint URL
            data: Request body
            headers: Request headers
            
        Returns:
            Response JSON or None
        """
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"API post error: {e}")
            return None
    
    def is_online(self) -> bool:
        """Check if internet connection is available"""
        try:
            response = self.session.get('https://www.google.com', timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def cache_get(self, key: str) -> Optional[Any]:
        """Get cached data"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now().timestamp() - timestamp < self.cache_duration:
                return data
            else:
                del self.cache[key]
        return None
    
    def cache_set(self, key: str, data: Any):
        """Cache data"""
        self.cache[key] = (data, datetime.now().timestamp())
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
