import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://eservices.ajmanded.ae/en/TradeLicense"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "eservices_ajmanded"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  


file_name = "2025-05-15/ajmanded/ajmanded.csv"

FILE_HEADERS = [
    "real_estate_link",
    "license_number",
    "license_type",
    "legal_form",
    "arabic_trade_name",
    "english_trade_name",
    "license_start_date" ,
    "license_expiry_date",
    "activities",
    "est_banning_status",
    "area"
]