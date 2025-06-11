import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
    "referer":"https://mmlafleur.com/"
}


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "mmlafleur"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  


file_name = "2025-06-10/mmLaFleur/mmlafleur.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "product_sku",
    "original_price",
    "sales_price",
    "category",
    "brand",
    "total_number_of_reviews",
    "star_1",
    "star_2",
    "star_3",
    "star_4",
    "star_5",
    "review_text"
]