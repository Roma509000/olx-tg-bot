import os
import time
import random as r
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import telebot
from telebot.types import InputMediaPhoto
from datetime import datetime


class OlxParser:
    def __init__(self, url):
        self.url = url

    def check_ids(self):
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--use-gl')
        options.add_argument('--disable-web-security')
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            options=options
        )

        driver.get(self.url)
        time.sleep(r.randint(2, 4))

        soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            ids = [int(id.find('div', class_='offer-wrapper').find('table')['data-id']) for id in
                   soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
            print('[INFO func: check_ids] Ids were taken successfully')
        except Exception as ex:
            print(f"[WARNING func: check_ids] Can't take ids: {ex}")
            ids = []

        return ids[:10][::-1]


    def get(self, start_id):
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--use-gl')
        options.add_argument('--disable-web-security')
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            options=options
        )

        driver.get(self.url)
        time.sleep(r.randint(2, 4))

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[10]/button').click()
            print('[INFO] Close the cookies window')
        except Exception as ex:
            print(f"[WARNING] Can't close cookies window: {ex}")

        soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            ids = [int(id.find('div', class_='offer-wrapper').find('table')['data-id']) for id in
                   soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
            print('[INFO] Ids were taken successfully')
        except Exception as ex:
            print(f"[WARNING] Can't take ids: {ex}")
            ids = []

        try:
            urls = [url.find("td", class_="photo-cell").find("a")["href"] for url in
                    soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
            print('[INFO] Urls were taken successfully')
        except Exception as ex:
            print(f"[WARNING] Can't take urls: {ex}")
            urls = []

        unprocessed_urls = []
        unprocessed_ids = []

        print(f'Start ids before: {start_id}')

        for id, url in zip(ids, urls):
            if id in start_id:
                break
            else:
                unprocessed_urls.append(url)
                unprocessed_ids.append(id)

        start_id.extend(unprocessed_ids[::-1])
        start_id = start_id[len(unprocessed_ids):]

        data_list = []
        for num, url in enumerate(unprocessed_urls, 1):
            try:
                driver.get(url)
                print('-' * 100)
                print(f'{num} url is gone: {url}')
                driver.execute_script("window.scrollTo(0, 400)")
                time.sleep(2)

                try:
                    show_phone = driver.find_element(By.CLASS_NAME, 'css-1i1450w-BaseStyles')
                    show_phone.click()
                    time.sleep(1)
                    print(f'[INFO page {num}] Pressed the phone button')
                except Exception as ex:
                    phone_number = ''
                    print(f"[WARNING page {num}] Can't press the phone button")

                page_soup = BeautifulSoup(driver.page_source, 'lxml')

                try:
                    count_pagination_buttons = len(page_soup.find_all('span', class_='swiper-pagination-bullet'))
                    for _ in range(count_pagination_buttons if count_pagination_buttons < 3 else 3):
                        driver.find_element(By.CSS_SELECTOR, 'button.swiper-button-next').click()
                        time.sleep(1)
                    print(f'[INFO page {num}] Swiped photos')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't swipe photos: {ex}")

                page_soup = BeautifulSoup(driver.page_source, 'lxml')

                try:
                    phone_number = page_soup.find('button', {'data-cy': 'ad-contact-phone'}).find('a')['href'].split(':')[1].strip()
                    print(f'[INFO page {num}] Found the phone number')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't find phone number: {ex}")
                    phone_number = ''

                try:
                    title = page_soup.find('h1', {'data-cy': 'ad_title'}).text.strip()
                    print(f'[INFO page {num}] Found a title')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't find title: {ex}")
                    title = ''

                try:
                    price = page_soup.find('div', {'data-testid': 'ad-price-container'}).find('h3').text.strip()
                    print(f'[INFO page {num}] Found a price')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't find price: {ex}")
                    price = ''

                try:
                    author = page_soup.find('h2', class_='css-u8mbra-Text eu5v0x0').text.strip()
                    print(f'[INFO page {num}] Found an author')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't find author: {ex}")
                    author = ''

                try:
                    photos_list = [photo.find('img')['srcset'] for photo in
                                   page_soup.find_all('div', {'data-cy': 'adPhotos-swiperSlide'})[:3]]
                    updated_photos_list = []

                    for photo in photos_list:
                        updated_photos_list.append(photo.split()[-2])
                    print(f'[INFO page {num}] Taken photos list')
                except Exception as ex:
                    print(f"[WARNING page {num}] Can't take photos list: {ex}")
                    updated_photos_list = []

                data = {
                    'title': title,
                    'price': price,
                    'phoneNumber': phone_number,
                    'author': author,
                    'photosList': updated_photos_list,
                    'url': url
                }

                if data['photosList']:
                    media_group = []
                    caption = f'<a href="{data["url"]}">{data["title"]}</a>\n' \
                              f'\n' \
                              f'<b>Ціна:</b> {data["price"]}\n' \
                              f'<b>Автор:</b> {data["author"]}\n' \
                              f'<b>Номер телефону:</b> {data["phoneNumber"] if data["phoneNumber"] else "<i>не вдалося отримати</i>"}\n'

                    for num, photo in enumerate(data['photosList']):
                        media_group.append(
                            InputMediaPhoto(photo, caption=caption if num == 0 else '', parse_mode='html'))

                    try:
                        bot.send_media_group(chat_id=CHANNEL_NAME, media=media_group)
                    except Exception as ex:
                        time.sleep(60)
                        bot.send_media_group(chat_id=CHANNEL_NAME, media=media_group)

                    time.sleep(2)

                elif data['title'] or data['price'] or data['phoneNumber'] or data['author']:
                    try:
                        bot.send_message(
                            chat_id=CHANNEL_NAME,
                            text=f'<a href="{data["url"]}">{data["title"]}</a>\n'
                                 f'\n'
                                 f'<b>Ціна:</b> {data["price"]}\n'
                                 f'<b>Автор:</b> {data["author"]}\n'
                                 f'<b>Номер телефону:</b> {data["phoneNumber"] if data["phoneNumber"] else "<i>не вдалося отримати</i>"}\n',
                            parse_mode='html'
                        )
                    except Exception as ex:
                        time.sleep(60)
                        bot.send_message(
                            chat_id=CHANNEL_NAME,
                            text=f'<a href="{data["url"]}">{data["title"]}</a>\n'
                                 f'\n'
                                 f'<b>Ціна:</b> {data["price"]}\n'
                                 f'<b>Автор:</b> {data["author"]}\n'
                                 f'<b>Номер телефону:</b> {data["phoneNumber"] if data["phoneNumber"] else "<i>не вдалося отримати</i>"}\n',
                            parse_mode='html'
                        )

            except Exception as ex:
                print(f'[WARNING] Page {url} not found: {ex}')
                continue

        print(f'Start ids after: {start_id}')
        return start_id

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME")
OLX_URL = os.environ.get("OLX_URL")

bot = telebot.TeleBot(BOT_TOKEN)

start_ids = OlxParser(url=OLX_URL).check_ids()
print(start_ids)
print()

while True:
    old_start_ids = start_ids
    try:
        start_ids= OlxParser(url=OLX_URL).get(start_id=start_ids)
    except Exception as ex:
        print(f"[WARNING] Wrong with getting data: {ex}")
        data_list = []

    print()
    print(f'Updated at: {str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split(".")[0]}')
    print(f"New start ids: {list(set(start_ids) - set(old_start_ids))}")
    print()

    time.sleep(r.randint(60, 90))
