import requests
from bs4 import BeautifulSoup
from settings import HEADERS


class DataMiningError(Exception):
    def __init__(self, message="An error occurred during data parsing."):
            self.message = message
            super().__init__(self.message)


class Flipkart:
    def __init__(self):
        self.url = None

    def start(self,url):
        self.url = url
        self.html_content = self.fetch_html()

    def fetch_html(self):
        try:
            response = requests.get(self.url,headers=HEADERS)
        except requests.ConnectionError:
            print("Connection error")
            return None
        except requests.HTTPError:
            print("Invalid response")
        except Exception:
            print("An error occurred")
            return None
        else:
            print("HTML content fetched successfully")
            return response.text
    
    def parse_data(self):
        try:
            soup = BeautifulSoup(self.html_content, "html.parser")

            brands = soup.find_all("div", class_="syl9yP")
            prices = soup.find_all("div", class_="Nx9bqj")
            images = soup.find_all('img', class_='_53J4C-')
            links = soup.find_all('a', class_='rPDeLR')

            self.brands = [b.get_text() for b in brands]
            self.prices = [p.get_text() for p in prices]
            self.img_urls = [img['src'] for img in images if img.has_attr('src')]
            self.product_url = ["https://www.flipkart.com" + a['href'] for a in links if a.has_attr('href')]
        
        except DataMiningError as e:
            print(e)
        except Exception:
            print("An error occurred")
    
    def parse_item(self):
        for b, p, img, url in zip(self.brands, self.prices, self.img_urls, self.product_url):
            yield {
                "Brand": b,
                "Price": p,
                "Image URL": img,
                "Product URL": url
            }
        
    def save_to_file(self):
        with open("2025-04-24/cleaned_data.txt", "w") as file:
            for item in self.parse_item():
                file.write(str(item)+"\n")
        print("Parsed data saved to file successfully")

        with open("2025-04-24/raw.html", "w") as file:
            file.write(self.html_content)
        print("Raw data saved to file successfully")
    
    def close(self):
        print("Closed the connection")

       
n = Flipkart()
n.start("https://www.flipkart.com/mens-footwear/sports-shoes/pr?sid=osp,cil,1cu&otracker=categorytree")
n.parse_data()
n.save_to_file()
n.close()