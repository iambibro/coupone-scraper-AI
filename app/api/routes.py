from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from app.scrapers.ajio_scraper import AjioScraper
from app.scrapers.myntra_scraper import MyntraScraper
from app.models.coupon import CouponResponse
import time

router = APIRouter()

# Create a registry of available scrapers
SCRAPERS = {
    "ajio": AjioScraper,
    "myntra": MyntraScraper
}

# Cache to store results to limit repeated scraping
coupon_cache = {}
CACHE_TTL = 3600  # Cache time-to-live in seconds (1 hour)

@router.get("/coupons", response_model=CouponResponse)
async def get_coupons(brand: str = Query(..., description="Brand name (e.g., Ajio, Myntra)")):
    """
    Get coupon codes for a specific brand
    """
    brand_lower = brand.lower()
    
    if brand_lower not in SCRAPERS:
        raise HTTPException(status_code=404, detail=f"Brand '{brand}' not supported. Available brands: {', '.join(SCRAPERS.keys())}")
    
    # Check cache first
    current_time = time.time()
    if brand_lower in coupon_cache and (current_time - coupon_cache[brand_lower]["timestamp"]) < CACHE_TTL:
        return coupon_cache[brand_lower]["data"]
    
    # If not in cache or cache expired, scrape fresh data
    try:
        scraper = SCRAPERS[brand_lower]()
        result = scraper.get_results()
        
        # Cache the result
        coupon_cache[brand_lower] = {
            "data": result,
            "timestamp": current_time
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping coupons: {str(e)}")

@router.get("/supported-brands")
async def get_supported_brands():
    """
    Get a list of supported brands
    """
    return {"supported_brands": list(SCRAPERS.keys())}
