import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.dubizzle.com.bh/en/properties/properties-for-sale/"


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "dubizzle"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  


file_name = "2025-05-16/dubizzle/dubizzle.csv"

FILE_HEADERS = [
    "url",
    "currency",
    "price",
    "beadroom",
    "bathroom",
    "furnished",
    "area",
    "location",
    "amenities",
    "price_type",
    "breadcrumb",
    "description",
    "images",
]