import requests
from parsel import Selector
from PIL import Image
from io import BytesIO
import pytesseract
import urllib3
import logging
from settings import HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://freesearchigrservice.maharashtra.gov.in/"
year = "2025"
district = "30"
village_input = "p"
property_no = "11"

session = requests.Session()
response = session.get(url, headers=HEADERS, verify=False)
sel = Selector(text=response.text)

viewstate = sel.xpath('//input[@name="__VIEWSTATE"]/@value').get()
eventvalidation = sel.xpath('//input[@name="__EVENTVALIDATION"]/@value').get()
viewstategen = sel.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').get()

payload_area = {
    '__EVENTTARGET': 'txtAreaName',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategen,
    '__EVENTVALIDATION': eventvalidation,
    'ddlFromYear': year,
    'ddlDistrict': district,
    'txtAreaName': village_input,
    'txtAttributeValue': '',
    'ddlareaname': '-----Select Area----',
    'txtImg': ''
}

res_area = session.post(url, headers=HEADERS, data=payload_area, verify=False)
sel_area = Selector(text=res_area.text)

viewstate = sel_area.xpath('//input[@name="__VIEWSTATE"]/@value').get()
eventvalidation = sel_area.xpath('//input[@name="__EVENTVALIDATION"]/@value').get()
viewstategen = sel_area.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').get()

village_options = sel_area.xpath('//select[@id="ddlareaname"]/option/text()').getall()
valid_areas = [v.strip() for v in village_options if v.strip() and "Select" not in v and v.lower().startswith(village_input.lower())]
selected_area = valid_areas[0]

logging.info(f"Selected Village: {selected_area}")

captcha_rel_url = sel_area.xpath('//img[@id="imgCaptcha"]/@src').get()
captcha_url = f"{url}{captcha_rel_url}"
captcha_img = session.get(captcha_url, headers=HEADERS, verify=False)
img = Image.open(BytesIO(captcha_img.content))
captcha_text = pytesseract.image_to_string(img).strip()

logging.info(f"CAPTCHA: {captcha_text}")

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

response = session.post(url, headers=HEADERS, data=payload_search, verify=False)

