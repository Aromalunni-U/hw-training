import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.dubizzle.com.bh/en/vehicles/cars-for-sale/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "dubizzle"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  


file_name = "dubizzle.csv"
