import requests
import time
from settings import HEADERS


def crawler(url):
    limit = 18
    total_advisors = 1010
    all_links = []


    for offset in range(0, total_advisors, limit):  
        params = {
            "sortKey": "firstname",
            "sortDir": "asc",
            "offset": offset,
            "limit": limit
        }

        print(f"Fetching offset {offset}...")

        response = requests.get(url, params=params, headers=HEADERS)
        response.raise_for_status() 

        data = response.json()
        advisors = data.get("records")

        for advisor in advisors:
            advisor_id = advisor.get("advisorId")
            if advisor_id:
                name = advisor.get("name")
                first_name = name.get("firstName")
                last_name = name.get("lastName")

                if first_name and last_name:
                    link = f"https://www.evrealestate.com/en/our-advisors/{first_name}-{last_name}/{advisor_id}"
                    all_links.append(link)

        time.sleep(0.5)

    return all_links
