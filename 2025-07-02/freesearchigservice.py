import requests
from parsel import Selector
from PIL import Image
from io import BytesIO
import pytesseract
import urllib3
import logging
from settings import HEADERS, villages

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://freesearchigrservice.maharashtra.gov.in/"

year = "2023"
district = "30"
village_input = "a"
property_no = "9"
selected_area = villages.get(village_input)[1] 


logging.info(f"Selected Village: {selected_area}")

res = requests.get(url, headers=HEADERS, verify=False)
sel = Selector(text=res.text)

viewstate = sel.xpath('//input[@name="__VIEWSTATE"]/@value').get()
eventvalidation = sel.xpath('//input[@name="__EVENTVALIDATION"]/@value').get()
viewstategen = sel.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').get()

# CAPTHCA
captcha_rel_url = sel.xpath('//img[@id="imgCaptcha"]/@src').get()
captcha_url = f"https://freesearchigrservice.maharashtra.gov.in/{captcha_rel_url}"
captcha_img = requests.get(captcha_url, headers=HEADERS, verify=False)
img = Image.open(BytesIO(captcha_img.content))
captcha_text = pytesseract.image_to_string(img)

logging.info(f"CAPTCHA : {captcha_text}")

payload_search = {
    '__EVENTTARGET': 'btnSearch',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategen,
    '__EVENTVALIDATION': eventvalidation,
    'ddlFromYear': year,
    'ddlDistrict': district,
    'txtAreaName': village_input,
    'ddlareaname': selected_area,
    'txtAttributeValue': property_no,
    'txtImg': captcha_text,
}

response = requests.post(url, headers=HEADERS, data=payload_search, verify=False)


logging.info(response.status_code)
