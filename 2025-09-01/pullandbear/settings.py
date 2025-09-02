import logging
from datetime import date


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.pullandbear.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}


PROJECT_NAME = "pullandbear"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "pullandbear"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

today = date.today().strftime("%Y_%m_%d")

file_name = f"2025-09-01/{PROJECT_NAME}/{PROJECT_NAME}_{today}.csv"

FILE_HEADERS = [ 
        "pdp_url",
        "prices",
        "product_id",
        "product_description",
        "color",
        "product_type"
]