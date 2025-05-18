# Helper utility functions

import re
from typing import List, Dict, Any, Optional
import os

def extract_coupon_codes(text: str) -> List[str]:
    """
    Extract potential coupon codes from text
    Assumes coupon codes are typically all caps or alphanumeric 
    with at least 4 characters
    """
    # Pattern for common coupon code formats
    patterns = [
        r'\b[A-Z0-9]{4,}\b',  # All caps alphanumeric, min 4 chars
        r'\b[A-Z]{3,}[0-9]{1,}\b',  # 3+ letters followed by 1+ numbers
        r'\b[A-Z0-9]{2,}[-_][A-Z0-9]{2,}\b',  # Codes with hyphens or underscores
    ]
    
    results = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            code = match.group(0)
            # Filter out common false positives
            if code not in ["HTTP", "HTML", "JSON", "HTTPS"] and len(code) <= 20:
                results.append(code)
    
    return list(set(results))  # Remove duplicates

def clean_description(text: str) -> str:
    """Clean and normalize offer descriptions"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Normalize currency symbols
    text = text.replace('Rs.', '₹').replace('Rs', '₹')
    
    # Normalize percentage symbols
    text = text.replace(' percent', '%').replace(' Percent', '%')
    
    return text

def parse_date(date_str: str) -> Optional[str]:
    """
    Parse various date formats into YYYY-MM-DD
    Returns None if parsing fails
    """
    if not date_str:
        return None
        
    # Try to handle common date formats
    patterns = [
        # DD/MM/YYYY or DD-MM-YYYY
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # MM/DD/YYYY or MM-DD-YYYY
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # YYYY/MM/DD or YYYY-MM-DD
        (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"),
    ]
    
    for pattern, formatter in patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                return formatter(match)
            except:
                continue
    
    # Handle textual dates
    months = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    
    # Pattern like "31 January 2025" or "January 31, 2025" or "31 Jan 2025"
    month_pattern = r'(\d{1,2})\s+([a-zA-Z]+)[\s,]+(\d{4})|([a-zA-Z]+)\s+(\d{1,2})[\s,]+(\d{4})'
    match = re.search(month_pattern, date_str, re.IGNORECASE)
    
    if match:
        groups = match.groups()
        if groups[0]:  # DD Month YYYY
            day, month_name, year = groups[0], groups[1], groups[2]
        else:  # Month DD YYYY
            month_name, day, year = groups[3], groups[4], groups[5]
            
        month_abbr = month_name[:3].lower()
        if month_abbr in months:
            return f"{year}-{months[month_abbr]}-{day.zfill(2)}"
            
    return None

def load_environment_variables():
    """Make sure required environment variables are set"""
    required_vars = ["OPENAI_API_KEY"]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("To use LLM features, set them in a .env file or environment.")
        return False
    
    return True

def get_default_model():
    """Get the default LLM model to use based on environment"""
    return os.getenv("DEFAULT_LLM_MODEL", "GPT-4.1")