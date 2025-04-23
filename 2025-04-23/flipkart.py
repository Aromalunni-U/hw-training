import requests
from bs4 import BeautifulSoup


class Flipkart:
    def __init__(self):
        self.url = None

    def start(self,url):
        self.url = url
        self.html_content = self.fetch_html()

    def fetch_html(self):

        try:
            response = requests.get(self.url)
        except requests.ConnectionError:
            print("Connection error")
            return None
        except Exception:
            print("An error occurred")
            return None
        else:
            print("HTML content fetched successfully")
            return response.text
    
    def parse_data(self):
        soup = BeautifulSoup(self.html_content, "html.parser")

        brands = soup.find_all("div", class_="syl9yP")
        prices = soup.find_all("div", class_="Nx9bqj")
        images = soup.find_all('img', class_='_53J4C-')
        links = soup.find_all('a', class_='rPDeLR')

        self.brands = [b.get_text() for b in brands]
        self.prices = [p.get_text() for p in prices]
        self.img_urls = [img['src'] for img in images if img.has_attr('src')]
        self.product_url = ["https://www.flipkart.com" + a['href'] for a in links if a.has_attr('href')]
    
   
    
    def parse_item(self):
        pass
      

    def save_to_file(self):
        parsed_data = f"Brand Name: {self.brands}\nPrice: {self.prices}\nImage URL: {self.img_urls}\nProduct URL: {self.product_url}"
        with open("cleaned_data.txt", "w") as file:
            file.write(parsed_data)
        print("Parsed data saved to file successfully")

        with open("raw.html", "w") as file:
            file.write(self.html_content)
        print("Raw data saved to file successfully")
    
    def close(self):
        print("Closed the connection")

       


n = Flipkart()
n.start("https://www.flipkart.com/mens-footwear/sports-shoes/pr?sid=osp,cil,1cu&otracker=categorytree")
n.parse_data()
n.save_to_file()
n.close()