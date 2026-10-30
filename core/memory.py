"""
API Handler for external integrations
Manages requests to external APIs
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime
from types import SimpleNamespace


class APIHandler:
    """Handles external API calls"""

    def __init__(self, config=None):
        self.config = config or SimpleNamespace(
            DEFAULT_LOCATION="New York",
            OPENWEATHER_API_KEY="",
            NEWS_API_KEY="",
            DEFAULT_COUNTRY_CODE="us",
        )
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 3600

    def fetch_weather(self, location: str = None, units: str = "metric") -> Optional[Dict]:
        try:
            location = location or getattr(self.config, 'DEFAULT_LOCATION', 'New York')
            api_key = getattr(self.config, 'OPENWEATHER_API_KEY', '')

            if not api_key or api_key == 'your_api_key_here':
                return {"error": "OpenWeather API key not configured"}

            url = "https://api.openweathermap.org/data/2.5/weather"
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
        try:
            api_key = getattr(self.config, 'NEWS_API_KEY', '')

            if not api_key or api_key == 'your_api_key_here':
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
                params["country"] = getattr(self.config, 'DEFAULT_COUNTRY_CODE', 'us')

            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"News API error: {e}")
            return None

    def search_wikipedia(self, query: str, auto_suggest: bool = True) -> Optional[Dict]:
        try:
            import wikipedia

            result = wikipedia.summary(query, auto_suggest=auto_suggest, sentences=3)
            return {
                "title": query,
                "summary": result,
                "source": "wikipedia"
            }

        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return None

    def fetch_data(self, url: str, params: Dict = None, headers: Dict = None) -> Optional[Dict]:
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"API fetch error: {e}")
            return None

    def post_data(self, url: str, data: Dict = None, headers: Dict = None) -> Optional[Dict]:
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"API post error: {e}")
            return None

    def is_online(self) -> bool:
        try:
            response = self.session.get('https://www.google.com', timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def cache_get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now().timestamp() - timestamp < self.cache_duration:
                return data
            else:
                del self.cache[key]
        return None

    def cache_set(self, key: str, data: Any):
        self.cache[key] = (data, datetime.now().timestamp())

    def clear_cache(self):
        self.cache.clear()

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass
