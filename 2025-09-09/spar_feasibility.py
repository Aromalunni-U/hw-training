from curl_cffi import requests


url = "https://api-scp.spar-ics.com/ecom/pw/v1/search/v1/navigation"

HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}


page_no = 1
category_name = "haushalt"

while True:

    params = {
        "query": "*",
        "sort": "Relevancy:asc",
        "page": page_no,
        "marketId": "NATIONAL",
        "showPermutedSearchParams": "false",
        "filter": f"pwCategoryPathIDs:{category_name}",
        "hitsPerPage": 32
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        impersonate="chrome"
    )
    
    if response.status_code == 200:

        data = response.json()

        hits = data.get("hits", [])
        paging = data.get("paging", {})
        page_count = paging.get("pageCount", "")

        if not hits or page_no > page_count:
            break

        for hit in hits:
            slug = hit.get("masterValues", {}).get("slug", "")
            if slug:
                pdp_url = f"https://www.spar.at/produktwelt/{slug}"
                print(pdp_url)

        page_no +=  1
        
    else:
        print(f"Status code : {response.status_code}")
        break
        
