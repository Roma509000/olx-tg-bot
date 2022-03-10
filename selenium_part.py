import time
import random as r
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pprint import pprint


class OlxParser:
    def __init__(self, url, start_id='661305865'):
        self.url = url
        self.start_id = int(start_id)


    def get(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--use-gl')
        options.add_argument('--disable-web-security')
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        options.add_extension(r'C:\Users\R3ynie\Desktop\olx-tg-bot\adblock.crx')

        driver = webdriver.Chrome(
            executable_path=r'C:\Users\R3ynie\Desktop\olx-tg-bot\chromedriver\chromedriver_win32\chromedriver.exe',
            options=options)

        driver.maximize_window()

        driver.get(self.url)
        try:
            driver.switch_to.window(window_name='CDwindow-D1204898AF6B72AD45AFB6021281AED5')
        except NoSuchWindowException:
            print('---')
        time.sleep(r.randint(4, 7))

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[10]/button').click()

            soup = BeautifulSoup(driver.page_source, 'lxml')

            try:
                ids = [int(id.find('div', class_='offer-wrapper').find('table')['data-id']) for id in
                       soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
            except Exception as ex:
                print(f'[WRONG with ids] {ex}')
                ids = []

            try:
                urls = [url.find("td", class_="photo-cell").find("a")["href"] for url in
                        soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
            except Exception as ex:
                print(f'[WRONG with urls] {ex}')
                urls = []

            unprocessed_urls = []

            for id, url in zip(ids, urls):
                if id == self.start_id:
                    break
                else:
                    unprocessed_urls.append(url)

            if len(unprocessed_urls) > 0:
                self.start_id = ids[0]

            data_list = []
            for url in unprocessed_urls:
                try:
                    driver.get(url)
                    time.sleep(2)

                    try:
                        show_phone = driver.find_element(By.CLASS_NAME, 'css-1i1450w-BaseStyles')
                        show_phone.click()
                        time.sleep(1)
                    except Exception as ex:
                        phone_number = ''

                    page_soup = BeautifulSoup(driver.page_source, 'lxml')

                    try:
                        count_pagination_buttons = len(page_soup.find_all('span', class_='swiper-pagination-bullet'))
                        for _ in range(count_pagination_buttons):
                            driver.find_element(By.CSS_SELECTOR, 'button.swiper-button-next').click()
                            time.sleep(1)
                    except Exception as ex:
                        print(ex)

                    page_soup = BeautifulSoup(driver.page_source, 'lxml')

                    try:
                        phone_number = page_soup.find('button', {'data-cy': 'ad-contact-phone'}).find('a')['href'].split(':')[1].strip()
                    except Exception as ex:
                        print(ex)
                        phone_number = ''

                    try:
                        title = page_soup.find('h1', {'data-cy': 'ad_title'}).text.strip()
                    except Exception as ex:
                        print(ex)
                        title = ''

                    try:
                        price = page_soup.find('div', {'data-testid': 'ad-price-container'}).find('h3').text.strip()
                    except Exception as ex:
                        print(ex)
                        price = ''

                    try:
                        author = page_soup.find('h2', class_='css-u8mbra-Text eu5v0x0').text.strip()
                    except Exception as ex:
                        print(ex)
                        author = ''

                    try:
                        photos_list = [photo.find('img')['srcset'] for photo in page_soup.find_all('div', {'data-cy': 'adPhotos-swiperSlide'})]
                        updated_photos_list = []

                        for photo in photos_list:
                            updated_photos_list.append(photo.split()[-2])
                    except Exception as ex:
                        print(ex)
                        updated_photos_list = []

                    data = {
                        'title': title,
                        'price': price,
                        'phoneNumber': phone_number,
                        'author': author,
                        'photosList': updated_photos_list,
                        'url': url
                    }
                    data_list.append(data)
                except Exception as ex:
                    print(f'[WRONG with url] Page not found: {url}\n{ex}')
                    continue

            return self.start_id, data_list
        except Exception as ex:
            print(f'[WRONG with switching windows]: {ex}')
            return





# pprint(OlxParser('https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5').get())


