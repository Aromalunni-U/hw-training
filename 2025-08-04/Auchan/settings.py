import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/friss-elelmiszer/tejtermek-tojas-sajt/csomagolt-sajtok.c-5680',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

cookies = {
        'AhuAU_C': '7ff85c1ef5ef3860738cb7b2520cb4c7431c59fb1ee568188bc41908b75f96bd',
        'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQz... (truncated)',
        'refresh_token': 'def50200e41d9701a67089e6ee0890612fb726afee00a2... (truncated)',
        'PHPSESSID': 'be3rbqpc255he2n5uqjtjlkts1',
    }