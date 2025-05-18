# Coupon Scraper API

A Python-based REST API that scrapes coupon codes from e-commerce websites using web scraping and AI-powered content extraction.

## Features

- Extracts coupon codes from various e-commerce websites
- API endpoints to fetch coupons by brand
- Uses AI to intelligently parse and extract coupon data
- Scalable architecture that can be extended with new brand scrapers
- Simple caching mechanism to avoid frequent scraping

## Project Structure

```
coupon-scraper/
├── app/
│   ├── __init__.py
│   ├── main.py                # Main FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API route definitions
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py    # Base scraper class
│   │   ├── ajio_scraper.py    # Ajio-specific scraper
│   │   └── myntra_scraper.py  # Myntra-specific scraper
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py         # Utility functions
│   └── models/
│       ├── __init__.py
│       └── coupon.py          # Data models
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (for LangChain integration)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coupon-scraper.git
cd coupon-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys (see `.env.example` for reference):
```bash
cp .env.example .env
# Edit .env file with your actual API keys
```

### Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

### API Documentation

Once the application is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Get Coupons by Brand

```
GET /api/coupons?brand={brand_name}
```

Example request:
```bash
curl -X GET "http://localhost:8000/api/coupons?brand=Ajio"
```

Example response:
```json
{
  "brand": "Ajio",
  "source": "https://www.ajio.com",
  "last_updated": "2025-05-17T12:30:45.123Z",
  "coupons": [
    {
      "code": "AJIO200",
      "description": "Up to 90% OFF + Extra ₹200 OFF on orders above ₹1199",
      "valid_till": "2025-05-30",
      "link": "https://www.ajio.com/shop/sale",
      "terms": "Minimum order value ₹1199"
    }
  ]
}
```

### Get Supported Brands

```
GET /api/supported-brands
```

Example response:
```json
{
  "supported_brands": ["ajio", "myntra"]
}
```

## Testing with Postman

1. Open Postman and create a new request
2. Set the method to GET and URL to `http://localhost:8000/api/coupons?brand=Ajio`
3. Send the request to see the coupon data response

## Adding New Brand Scrapers

To add support for a new e-commerce website:

1. Create a new scraper class in the `app/scrapers/` directory that inherits from `BaseScraper`
2. Implement the `extract_coupons()` method
3. Register the new scraper in `app/api/routes.py` by adding it to the `SCRAPERS` dictionary

## Future Enhancements

- Database integration with PostgreSQL
- User authentication
- Scheduled scraping jobs
- Vector search with pgvector
- Dockerization for easy deployment

## License

This project is licensed under the MIT License - see the LICENSE file for details.