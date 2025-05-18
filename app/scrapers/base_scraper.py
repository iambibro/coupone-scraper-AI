from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from app.models.coupon import Coupon

class BaseScraper(ABC):
    """Base scraper class that all brand-specific scrapers should inherit from"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.ua = UserAgent()
        
    def get_headers(self) -> Dict[str, str]:
        """Get random user agent headers to avoid detection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def fetch_page(self, url: str = None) -> BeautifulSoup:
        """Fetch HTML content from the given URL or base URL"""
        target_url = url if url else self.base_url
        
        try:
            response = requests.get(target_url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {target_url}: {e}")
            return BeautifulSoup("", 'lxml')  # Return empty soup on error
    
    @abstractmethod
    def extract_coupons(self) -> List[Coupon]:
        """Extract coupons from the target website, to be implemented by child classes"""
        pass

    def get_brand_name(self) -> str:
        """Get the brand name from the scraper"""
        return self.__class__.__name__.replace('Scraper', '')
    
    def get_results(self) -> Dict[str, Any]:
        """Get structured results with brand, source, and coupons"""
        coupons = self.extract_coupons()
        
        return {
            "brand": self.get_brand_name(),
            "source": self.base_url,
            "last_updated": datetime.now(),
            "coupons": coupons
        }