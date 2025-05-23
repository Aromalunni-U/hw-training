import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.plus.nl/screenservices/ECP_Composition_CW/ProductLists/PLP_Content/DataActionGetProductListAndCategoryInfo"
BASE_API_URL = "https://www.plus.nl/ECOP_HotCache_Eng/rest/ResourceManagement/Preload?url={}"

HEADERS = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "https://www.plus.nl",
    "Referer": "https://www.plus.nl/producten/frisdrank",
    "x-csrftoken": "T6C+9iB49TLra4jEsMeSckDMNhQ=", 
}

PARSER_HEADER = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "content-type":"text/plain; charset=utf-8"
}

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "plus"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  

file_name = "2025-05-23/plus/plus.csv"