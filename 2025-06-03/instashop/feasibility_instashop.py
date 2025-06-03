from playwright.sync_api import sync_playwright 

url = "https://instashop.com/en-ae/client/choithrams-safa-park/category/OfsKYyAZpW"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")

    page.wait_for_selector("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll", timeout=10000)
    button = page.locator("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    button.scroll_into_view_if_needed()
    button.click(force=True)

    page.wait_for_selector(".product.ng-star-inserted", timeout=30000) 

    html = page.content()
    
    browser.close()

