import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

HEADERS = {
    "authority": "www2.hm.com",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "upgrade-insecure-requests": "1",
}

PROJECT_NAME = "hm"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "hm"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"

file_name = "2025-06-30/hm/hm.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "regular_price",
    "art_number",
    "material_composition",
    "clothing_length",
    "clothing_fit",
    "country_of_origin",
    "neck_style",
    "style",
    "care_instruction",
    "color",
    "sleeve_length_style",
    "images"
]