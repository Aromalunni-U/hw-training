import requests
import xml.etree.ElementTree as ET
import logging
from settings import HEADERS, sitemap_url


response = requests.get(url=sitemap_url, headers= HEADERS)

root = ET.fromstring(response.content)


namespace = {"ns":"http://www.sitemaps.org/schemas/sitemap/0.9"}

for url_tag in root.findall("ns:url",namespaces=namespace):
    loc = url_tag.find("ns:loc",namespaces=namespace)
    pdp_url = loc.text
    logging.info(pdp_url)
    

