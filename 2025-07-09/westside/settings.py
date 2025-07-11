import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.westside.com"

filter_url = "https://westside-api.wizsearch.in/v1/products/filter"


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://www.westside.com",
    "Referer": "https://www.westside.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-api-key": "SzVuZVRLNUtKUDA5dlN5QUxBblUvTkdrY1c0bHpIanFWQnFVa1pBVklCZ3ZJWGtMdW5KdGZrMzM4ODJDM25FUGVQN2NxWlh3TVdoNFJ4UVptdXlKS2c9PQ==",
    "x-request-id": "7dab65f4-a342-4dd3-bf80-72c62bc0f8c6",
    "x-store-id": "2532b1c019c111f090410a0c8095feae",
    "x-wizzy-sessionid": "fbc1cb78-d2be-4c7a-8523-6aafb8d01edd",
    "x-wizzy-tags": "Device:Desktop,Platform:Linux",
    "x-wizzy-userid": "b235fc16-e7de-449f-9ce2-eb9fc28cecbb"
}

PROJECT_NAME = "westside"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "westside"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-07-09/westside/westside.csv"


FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "regular_price",
    "brand",
    "country_of_origin",
    "description",
    "care_instructions",
    "material_composition",
    "clothing_fit",
    "images",           
    "color",            
    "breadcrumb",
    "sku",
    "size"             
]