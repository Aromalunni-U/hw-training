import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS =  {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjU5NTBjN2UzNGI4MjdjNDE5OTAyNzExNTUwZWZmZDc0OGZkNThmNjQxMmI2OTRiZTM4Njg1NDY4Zjc0MTI1NjVmZjE2ODY5Y2FlMGY0NGJmIiwiaWF0IjoxNzU0Mjk5OTA0LjkyMDgzNywibmJmIjoxNzU0Mjk5OTA0LjkyMDg0MSwiZXhwIjoxNzU0Mzg2MzA0Ljg5Njg5Mywic3ViIjoiYW5vbl84ZGU2YTI3NS03NWFiLTQxODktYjk3YS0zNjBjN2NhYzU1ZDkiLCJzY29wZXMiOltdfQ.JvY1fX7QfpQ94KcJuDlCecW8foBGL5WTU1yGURA9EK18gBuYfDQxxJqWVux2V8dKVO6M2Oc0M4FePzDaeIT49em33j1V7cuS2HD0iAz5Ieg6qUtgjfsdHdljYDrjd1zJvJZfxQjJZ_wRncvSk0VgirGmPFcnpLXbyze1UzwNgr1IAD3XEqf23ttTA8ClrZMtQ3DrcR5J9Nha89iWR6u18rIFO7rbEldcy1oBmjzbryV_x2FCyeX62-_OY22lOav_AIQhf6zJcnU3i5pGbvEWlLg--pjKV3ejxDfpcADczv7enbwUoC0zalp712WZ02bySPyIUbvMaAD24Toflu3APA',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}


cookies = {
    'login_type': 'anon',
    'isWebpFormatSupportedAlgo0': 'true',
    'token_type': 'Bearer',
    'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjU5NTBjN2UzNGI4MjdjNDE5OTAyNzExNTUwZWZmZDc0OGZkNThmNjQxMmI2OTRiZTM4Njg1NDY4Zjc0MTI1NjVmZjE2ODY5Y2FlMGY0NGJmIiwiaWF0IjoxNzU0Mjk5OTA0LjkyMDgzNywibmJmIjoxNzU0Mjk5OTA0LjkyMDg0MSwiZXhwIjoxNzU0Mzg2MzA0Ljg5Njg5Mywic3ViIjoiYW5vbl84ZGU2YTI3NS03NWFiLTQxODktYjk3YS0zNjBjN2NhYzU1ZDkiLCJzY29wZXMiOltdfQ.JvY1fX7QfpQ94KcJuDlCecW8foBGL5WTU1yGURA9EK18gBuYfDQxxJqWVux2V8dKVO6M2Oc0M4FePzDaeIT49em33j1V7cuS2HD0iAz5Ieg6qUtgjfsdHdljYDrjd1zJvJZfxQjJZ_wRncvSk0VgirGmPFcnpLXbyze1UzwNgr1IAD3XEqf23ttTA8ClrZMtQ3DrcR5J9Nha89iWR6u18rIFO7rbEldcy1oBmjzbryV_x2FCyeX62-_OY22lOav_AIQhf6zJcnU3i5pGbvEWlLg--pjKV3ejxDfpcADczv7enbwUoC0zalp712WZ02bySPyIUbvMaAD24Toflu3APA',
    '_omappvp': 'zmJOsflS6Mzpw5CJFreCVsjJXB1KwYgkgoKEcJdmBrlNxT4922PL5PXcfdyVJJzRTNKyBGhMpqVr1uKZHsMLqF54gNHMxhEQ',
    'optiMonkClientId': 'f1230534-e0d0-a928-9428-fd217cc542e7',
    'OptanonAlertBoxClosed': '2025-08-04T09:35:26.873Z',
    '_gcl_au': '1.1.421426614.1754300127',
    '_ga': 'GA1.1.1614842446.1754299913',
    '_fbp': 'fb.1.1754300129874.601315702576240320',
    '_hjSessionUser_888997': 'eyJpZCI6IjhlYjhjNGNlLTQ3MmUtNTIyNy1hMmFlLWQ4ZGYwNmNmZjczMSIsImNyZWF0ZWQiOjE3NTQzMDAxMzEwNDcsImV4aXN0aW5nIjp0cnVlfQ==',
    'AhuAU_C': '7ff85c1ef5ef3860738cb7b2520cb4c7431c59fb1ee568188bc41908b75f96bd',
    'aw_notification_info': '%7B%7D',
    '_clck': 'u1xr0a%7C2%7Cfy7%7C0%7C2042',
    '_hjSession_888997': 'eyJpZCI6IjI1ZmJmZWIyLWRlYzItNGVkOS1hNjMwLTY2ZTdkMDFjNTc4NCIsImMiOjE3NTQzNjU0ODQ2NzYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    'tfpsi': '2b27820a-1e84-43af-9fb7-850973428340',
    'PHPSESSID': '0jtagv9nj11cjpb1unmjfol3i5',
    '_ga_XTT3C4HH22': 'GS2.1.s1754365480$o2$g1$t1754365804$j60$l0$h0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Aug+05+2025+09%3A20%3A06+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=e8933271-18a0-4a82-a02c-ac2b71485bef&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false',
    '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-08-05T03%3A50%3A07.976Z%22%7D',
    '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22jB39c9DMqSYKXGbMwOKA%22%2C%22expiryDate%22%3A%222026-08-05T03%3A50%3A07.976Z%22%7D',
    'optiMonkClient': 'N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8sALGAJx2mz4A2JS5VEAbLFAAxQA6XvCj4AdgHsADqzC9s2IA==',
    '_clsk': 's07pf%7C1754365827041%7C3%7C1%7Ca.clarity.ms%2Fcollect',
}


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "auchan"
DATA_COLLECTION = "parser"

file_name = "2025-08-04/Auchan/auchan.csv"

FILE_HEADERS = [
    "unique_id",
    "product_name",
    "regular_price",
    "selling_price",
    "percentage_discount",
    "breadcrumb",
    "pdp_url",
    "uom"
]