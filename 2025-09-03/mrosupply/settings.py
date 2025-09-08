import logging
from datetime import date


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}



PROJECT_NAME = "mrosupply"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "mrosupply"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

today = date.today().strftime("%Y_%m_%d")

file_name = f"2025-09-03/{PROJECT_NAME}/{PROJECT_NAME}_{today}.csv"

FILE_HEADERS = [
    "Company Name",
    "Manufacturer Name",
    "Brand Name",
    "Manufacturer Part Number",
    "Vendor/Seller Part Number",
    "Item Name",
    "Full Product Description",
    "Price",
    "Country of Origin",
    "Unit of Issue",
    "QTY Per UOI",
    "UPC",
    "Model Number",
    "Product Category",
    "URL",
    "Availability",
    "Date Crawled"
]