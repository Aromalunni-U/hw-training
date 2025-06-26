import requests
from xml.dom.minidom import parseString
import logging
from settings import HEADERS, sitemap_url

response = requests.get(sitemap_url, headers=HEADERS)
dom = parseString(response.content)

for loc in dom.getElementsByTagName("loc"):
    url = loc.firstChild.data
    logging.info(url)