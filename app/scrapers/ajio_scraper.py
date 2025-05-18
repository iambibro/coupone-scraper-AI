from app.scrapers.base_scraper import BaseScraper
from app.models.coupon import Coupon
from typing import List
import re
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

class AjioScraper(BaseScraper):
    """Scraper for Ajio website"""
    
    def __init__(self):
        # super().__init__("https://www.ajio.com")
        super().__init__("https://www.coupondunia.in/ajio")
        # Adding an alternative URL that may contain coupons (offers page)
        # self.offers_url = "https://www.ajio.com/help/offers"
        self.offers_url = "https://www.coupondunia.in/ajio"
        
    def extract_coupons(self) -> List[Coupon]:
        """Extract coupons from Ajio website"""
        coupons = []
        
        # First try the main page
        soup = self.fetch_page()
        if soup:
            # Look for coupon banners, promo sections
            promo_sections = soup.find_all(class_=lambda x: x and ('promo' in x.lower() or 'coupon' in x.lower() or 'offer' in x.lower()))
            coupons.extend(self._process_html_sections(promo_sections))
        
        # Then try the offers page
        soup = self.fetch_page(self.offers_url)
        if soup:
            # Look for offer sections
            offer_sections = soup.find_all(class_=lambda x: x and ('offer' in x.lower() or 'coupon' in x.lower() or 'promo' in x.lower()))
            coupons.extend(self._process_html_sections(offer_sections))
        
        return coupons
    
    def _process_html_sections(self, sections) -> List[Coupon]:
        """Process HTML sections to extract coupon data using LLM"""
        if not sections:
            return []
            
        coupons = []
        html_content = '\n'.join(str(section) for section in sections)
        
        # Use LLM to extract coupon information
        llm_coupons = self._extract_with_llm(html_content)
        coupons.extend(llm_coupons)
        
        return coupons
    
    def _extract_with_llm(self, html_content: str) -> List[Coupon]:
        """Use LLM to extract coupon data from HTML content"""
        try:
            # Initialize the LLM
            llm = ChatOpenAI(temperature=0, model_name="GPT-4.1")
            
            # Create a parser for the Coupon model
            parser = PydanticOutputParser(pydantic_object=Coupon)
            
            # Create a prompt template
            prompt_template = PromptTemplate(
                input_variables=["html_content"],
                template="""
                You are an expert in extracting coupon information from HTML content.
                Extract all coupon codes and related information from the following HTML content:
                
                {html_content}
                
                For each coupon, extract:
                1. The coupon code (like "AJIO200", "FIRST50", etc.)
                2. A detailed description of what the coupon offers
                3. Valid till date if available (in YYYY-MM-DD format)
                4. Any link that applies the coupon if available
                5. Any terms or conditions if available
                
                Format your response as JSON objects with the following fields:
                - code: The coupon code
                - description: Detailed description of the offer
                - valid_till: Expiration date in YYYY-MM-DD format (optional)
                - link: URL to apply the coupon (optional)
                - terms: Any terms or conditions (optional)
                
                Return the data as a list of dictionaries within square brackets. Example:
                [
                    {
                        "code": "AJIO200",
                        "description": "Up to 90% OFF + Extra ₹200 OFF on orders above ₹1199",
                        "valid_till": "2025-04-30",
                        "link": "https://www.ajio.com/...",
                        "terms": "Minimum order value ₹1199"
                    }
                ]
                If no coupons are found, return an empty list: []
                """
            )
            
            # Process the HTML content with the LLM
            llm_output = llm.invoke(prompt_template.format(html_content=html_content[:4000]))  # Limit size of content
            
            # Parse the output - handle both string format and already parsed format
            content = llm_output.content if hasattr(llm_output, 'content') else llm_output
            
            # Attempt to extract JSON from the response
            json_match = re.search(r'\[\s*{.*}\s*\]', content, re.DOTALL)
            
            if json_match:
                import json
                try:
                    coupon_data = json.loads(json_match.group(0))
                    return [Coupon(**coupon) for coupon in coupon_data]
                except json.JSONDecodeError:
                    print("Failed to parse LLM output as JSON")
                    return []
            else:
                print("No valid JSON found in LLM output")
                return []
                
        except Exception as e:
            print(f"Error in LLM extraction: {e}")
            return []
            
    def get_brand_name(self) -> str:
        """Override to return the proper brand name"""
        return "Ajio"