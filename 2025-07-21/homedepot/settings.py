import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.homedepot.com/"

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


headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://www.homedepot.com",
    "Referer": "https://www.homedepot.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "X-API-Cookies": '{"x-user-id":"6e143175-d7f1-9520-b042-1154d1f7bcf8"}',
    "X-Cloud-Trace-Context": "a85ef686dc4d4ce28cca64b0c68fa00a/1;o=1",
    "X-Current-Url": "/b/Electrical-Wire/N-5yc1vZbm7v",
    "X-Debug": "false",
    "X-Experience-Name": "general-merchandise",
    "X-HD-DC": "origin",
    "X-Parent-Trace-Id": "af965de74956a5c7c4a3ee8b8ac711d8/4101720202215077614",
    "Accept": "application/json",
    "Pragma": "no-cache",
    "Priority": "u=1, i"
}

PROJECT_NAME = "homedepot"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "homedepot"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-07-21/homedepot/homedepot.csv"


FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "brand",
    "breadcrumb",
    "retail_limit",
    "currency",
    "selling_price",
    "price_was",
    "images",
    "rating",
    "review",
    "product_description",
    "product_details"
]