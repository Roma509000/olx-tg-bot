from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from pprint import pprint
import pickle

class OlxScraper:

    def __init__(self):
        # changing user-agent
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

        # disable webdriver mode
        options.add_argument('--disable-blink-features=AutomationControlled')

        # enable headless mode
        # options.add_argument('--headless')

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--use-gl')
        options.add_argument('--disable-web-security')
        options.add_experimental_option("excludeSwitches", ['enable-logging'])

        self.driver = webdriver.Chrome(
            executable_path=r'C:\Users\R3ynie\Desktop\olx-tg-bot\chromedriver\chromedriver_win32\chromedriver.exe',
            options=options
        )

        self.driver.maximize_window()

    def check_general_announcement(self, url, start_url):
        self.driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        urls = [url.find("td", class_="photo-cell").find("a")["href"] for url in soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]

        unprocessed_urls = []

        for page_url in urls:
            if page_url.split('.html')[0] in start_url:
                break
            else:
                unprocessed_urls.append(page_url)

        data = []
        for page_url in unprocessed_urls:
            try:
                self.driver.get(page_url)
                self.driver.execute_script("window.scrollTo(0, 400)")
                time.sleep(1)

                show_phone = self.driver.find_element(By.CLASS_NAME,'css-1i1450w-BaseStyles')
                show_phone.click()
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                title = soup.find('h1', {'data-cy': 'ad_title'}).text.strip()
                price = soup.find('div', {'data-testid': 'ad-price-container'}).find('h3').text.strip()
                phone_number = soup.find('button', {'data-cy': 'ad-contact-phone'}).find('a')['href'].split(':')[1].strip()
                author = soup.find('h2', class_='css-u8mbra-Text eu5v0x0').text.strip()


                data.append(
                    {
                        'title': title,
                        'price': price,
                        'phoneNumber': phone_number,
                        'url': page_url,
                        'author': author
                    }
                )



            except Exception as ex:
                print(ex)
                continue

        return unprocessed_urls[0], data


# pprint(OlxScraper().check_general_announcement(
#     url='https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5?page=1',
#     start_url='https://www.olx.ua/d/uk/obyavlenie/3-kmn-komarova-gerov-maydanu-IDMi4yR.html#000d3b0210'
# ))





