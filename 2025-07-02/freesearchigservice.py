import requests
from parsel import Selector
from PIL import Image
from io import BytesIO
import pytesseract
import urllib3
import logging
from settings import HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_tokens(sel):
    viewstate = sel.xpath('//input[@name="__VIEWSTATE"]/@value').get()
    viewstategen = sel.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').get()
    eventvalidation = sel.xpath('//input[@name="__EVENTVALIDATION"]/@value').get()

    return {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategen,
        "__EVENTVALIDATION": eventvalidation
    }

BASE_URL = "https://freesearchigrservice.maharashtra.gov.in/"

year = "2025"
district = "30"
village_input = "p"
property_no = "11"

session = requests.Session()
response = session.get(BASE_URL, headers=HEADERS, verify=False)
sel = Selector(text=response.text)


tokens = extract_tokens(sel)

payload_area = {
    '__EVENTTARGET': 'txtAreaName',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    **tokens,
    'ddlFromYear': year,
    'ddlDistrict': district,
    'txtAreaName': village_input,
    'txtAttributeValue': '',
    'ddlareaname': '-----Select Area----',
    'txtImg': ''
}

res_area = session.post(BASE_URL, headers=HEADERS, data=payload_area, verify=False)
sel = Selector(text=res_area.text)
tokens = extract_tokens(sel)

village_options = sel.xpath('//select[@id="ddlareaname"]/option/text()').getall()
valid_areas = [v.strip() for v in village_options if v.strip() and "Select" not in v and v.lower().startswith(village_input.lower())]


selected_area = valid_areas[0]
logging.info(f"Selected area: {selected_area}")

payload_area_select = {
    '__EVENTTARGET': 'ddlareaname',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    **tokens,
    'ddlFromYear': year,
    'ddlDistrict': district,
    'txtAreaName': village_input,
    'ddlareaname': selected_area,
    'txtImg': ''
}

res_area_select = session.post(BASE_URL, headers=HEADERS, data=payload_area_select, verify=False)
sel = Selector(text=res_area_select.text)
tokens = extract_tokens(sel)

captcha_url = sel.xpath('//img[@id="imgCaptcha"]/@src').get()
captcha_url = f"{BASE_URL}{captcha_url}"
captcha_img = session.get(captcha_url, headers=HEADERS, verify=False)
img = Image.open(BytesIO(captcha_img.content))
captcha_text = pytesseract.image_to_string(img).strip()

logging.info(f"CAPTCHA: {captcha_text}")

HEADERS.update({
    "X-MicrosoftAjax": "Delta=true",
    "X-Requested-With": "XMLHttpRequest"
})

payload_search = {
    "ScriptManager1": "UpMain|btnSearch",
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__LASTFOCUS": "",
    **tokens,
    "__ASYNCPOST": "true",
    "ddlFromYear": year,
    "ddlDistrict": district,
    "txtAreaName": village_input,
    "ddlareaname": selected_area,
    "txtAttributeValue": property_no,
    "txtImg": captcha_text,
    "FS_PropertyNumber": "",
    "FS_IGR_FLAG": "",
    "btnSearch": "शोध / Search"
}

response = session.post(BASE_URL, headers=HEADERS, data=payload_search, verify=False)
sel = Selector(text = response.text)

tokens = extract_tokens(sel)


indexii_buttons = sel.xpath("//input[@value='IndexII']/@onclick").getall()
logging.info(indexii_buttons)

index = 'indexII$2'

payload_index = {
    "ScriptManager1": "upRegistrationGrid|RegistrationGrid",
    "__EVENTTARGET": "RegistrationGrid",
    "__EVENTARGUMENT": index,
    "__LASTFOCUS": "",
    **tokens,
    "__ASYNCPOST": "true",
    "ddlFromYear": year,
    "ddlDistrict": district,
    "txtAreaName": village_input,
    "ddlareaname": selected_area,
    "txtAttributeValue": property_no,
    "txtImg": captcha_text,
    "FS_PropertyNumber": "",
    "FS_IGR_FLAG": ""
    }

res_index = session.post(BASE_URL, headers=HEADERS, data=payload_index, verify=False)

url = "https://freesearchigrservice.maharashtra.gov.in/rptIndex2_regLive.aspx"

response = session.get(url, headers=HEADERS, verify=False)




