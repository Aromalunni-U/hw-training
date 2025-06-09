import requests
from parsel import Selector


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

ean_list = [
    "76344107521", "76344107491", "76344108115", "76344107538", "76344118572",
    "76344105398", "76344107262", "76344108320", "76344116639", "76344106661",
    "64992523206", "64992525200", "64992523602", "64992525118", "64992714369",
    "64992714376", "64992719814", "64992719807", "5060184240512", "5060184240703",
    "5060184240598", "5060184244909", "5060184240109", "5425039485256", "5425039485010",
    "5425039485263", "5425039485034", "5425039485317", "5407009646591", "5407009640353",
    "5407009640391", "5407009640636", "5407009641022", "3182551055672", "3182551055788",
    "3182551055719", "3182551055825", "9003579008362", "3182550704625", "3182550706933",
    "9003579013793", "9003579013861"
]

search_url = "https://www.diebo.nl/assortiment?q={}&action=getAjaxSearchArtikelen"

exists_count = 0
not_found_count = 0
found = []

for ean in ean_list:
    url = search_url.format(ean)
    response = requests.get(url, headers=HEADERS)
    sel = Selector(response.text)

    if response.status_code == 200:
        links = sel.xpath("//a[@class='full-link']/@href").getall()
        if links:
            links = ["https://www.diebo.nl/" + url for url in links]
            print(f"EAN: {ean} URL: {links}")
            exists_count += 1
        else:
            not_found_count += 1
        

total_count = len(ean_list)

print(f"Not Found Count: {not_found_count}")
print(f"Failure Percentage: {(not_found_count / total_count) * 100:.2f}%")
print(f"Success Percentage: {(exists_count / total_count) * 100:.2f}%")
