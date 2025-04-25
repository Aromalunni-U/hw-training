import requests
from parsel import Selector


url = "https://www.marksandspencer.com/l/men/mens-shirts#intid=gnav_men_core_clothing_shirts"

response = requests.get(url)

if response.status_code == 200:
    try:
      selector = Selector(response.text)
      product_link = selector.xpath("//a[@class='product-card_cardWrapper__GVSTY']/@href").getall()
      category = selector.xpath("//h1[contains(@class,'media-0_headingMd__1TuR5')]/text()").get()
      page = selector.xpath("//a[@class='pagination_trigger__YEwyN']/@href").get()

      print(f"Product Link: {product_link}")
      print(f"Category: {category}")  
      print(f"Page: {page}")
      
    except Exception as e:
        print(f"An error occurred: {e}")  
