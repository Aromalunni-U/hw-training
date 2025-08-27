import logging


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

cookies = {
        'JSESSIONID': 'hY7qA1KsKJbQKQXjPOBiybfLRU5LNDC3nY0ri2MdggegW39WKdKY!18651468',
        'WWW-WS-ROUTE': 'ffffffff09c20e0b45525d5f4f58455e445a4a4216cf',
        '_pxvid': '1148e41a-8239-11f0-ac1b-4d3d4bfcc486',
        '_px2': 'eyJ1IjoiMGM5ZDRiZTEtODMwYy0xMWYwLWFkNGMtMGJhMjgyZjA2ZjAzIiwidiI6IjExNDhlNDFhLTgyMzktMTFmMC1hYzFiLTRkM2Q0YmZjYzQ4NiIsInQiOjE3NTYyNzUzMjUwOTcsImgiOiI1NjEyMDA3ZGFlN2M5NzZlNmJiMWI2YmEyYjgyYjQzMzA2NzU5ZmMxNDBmMjMxZmJiYmFhNmYyYjBhZmViZWRiIn0=',
        '_pxdc': 'Bot',
        'botStatus': 'Not a Bot'
}


PROJECT_NAME = "autozone"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "autozone"
INTEREXCHANGE_DATA = "interexchange_number_data"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
NO_MATCHED_COLLECTION = "no_matched_parts"

file_name = "2025-08-26/autozone/autozone.csv"
