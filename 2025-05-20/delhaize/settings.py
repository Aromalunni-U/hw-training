import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_API_URL = "https://www.delhaize.be/api/v1/"


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "delhaize"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  


FILE_HEADERS = [
    "product_url",
    "name",
    "product_code",
    "currency",
    "price",
    "price_per_unit",
    "description",
    "imges_url" 
]