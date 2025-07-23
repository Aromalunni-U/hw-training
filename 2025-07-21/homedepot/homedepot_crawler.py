import requests
import logging
from homedepot_items import  ProductUrlItem
from mongoengine import connect
from settings import headers, DB_NAME, MONGO_URI
import json
import time


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):

        api_url = "https://apionline.homedepot.com/federation-gateway/graphql?opname=searchModel"

        start_index = 0
        page_size = 48  

        while True:
            payload = {
                "operationName": "searchModel",
                "variables": {
                    "navParam": "N-5yc1vZbqsi",
                    "storeId": "1710",
                    "channel": "DESKTOP",
                    "orderBy": {
                        "field": "TOP_SELLERS",
                        "order": "ASC"
                    },
                    "startIndex": start_index,
                    "pageSize": page_size,
                    "additionalSearchParams": {
                        "deliveryZip": "96913"
                    }
                },
                "query": """
                    query searchModel(
                        $storeId: String, $startIndex: Int, $pageSize: Int,
                        $orderBy: ProductSort, $navParam: String, $channel: Channel,
                        $additionalSearchParams: AdditionalParams
                    ) {
                        searchModel(
                            storeId: $storeId
                            navParam: $navParam
                            channel: $channel
                            additionalSearchParams: $additionalSearchParams
                        ) {
                            products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy) {
                                identifiers {
                                    productLabel
                                    modelNumber
                                    canonicalUrl
                                    brandName
                                }
                            }
                        }
                    }
                """
            }

            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                data = response.json()

                try:
                    products = data.get("data", {}).get("searchModel", {}).get("products", [])
                except:
                    break

                if not products:
                    break

                for product in products:
                    url = product.get("identifiers", {}).get("canonicalUrl", "")
                    url = f"https://www.homedepot.com{url}"
                    logging.info(url)

                    try:
                        ProductUrlItem(url = url).save()
                    except:
                        pass
                
                start_index += page_size
                time.sleep(0.5)
            else:
                logging.error(f"Status code {response.status_code}")
                break


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()