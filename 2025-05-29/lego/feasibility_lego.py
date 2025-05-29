import requests
from parsel import Selector


headers = {
    "accept-encoding":"gzip, deflate",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}



###################### CRAWLER #########################

url = "https://www.lego.com/en-in/categories/all-sets"

response = requests.get(url,headers=headers)

print(response.text)
response = Selector(response.text)

products_urls = response.xpath(
    '//div[@data-test="product-leaf-action-row"]/a/@href'
    ).getall()

print(products_urls)

###################### PARSER ###########################

url = "https://www.lego.com/en-in/product/venator-class-republic-attack-cruiser-75367"

response = requests.get(url=url,headers=headers)

response = Selector(response.text)

product_name_xpath = '//h1[@data-test="product-overview-name"]/span/text()'
breadcrumb_xpath = '//ol[contains(@class, "breadcrumbList")]//li'
ages_xpath = ""

product_name = response.xpath(product_name_xpath).get()
raw_breadcrumb = response.xpath(breadcrumb_xpath)
ages = response.xpath(ages_xpath).get()

breadcrumb = []
for li in raw_breadcrumb:
    text = li.xpath('string(.//span[@data-test="markup"])').get().strip()
    breadcrumb.append(text)

print(ages)

