from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Coupon(BaseModel):
    code: str
    description: str
    valid_till: Optional[str] = None
    link: Optional[str] = None
    terms: Optional[str] = None
    
class CouponResponse(BaseModel):
    brand: str
    source: str
    last_updated: datetime
    coupons: List[Coupon]