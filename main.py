from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import telebot
import threading
import time
import random

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

driver = webdriver.Chrome(
                executable_path=r'C:\Users\R3ynie\Desktop\olx-tg-bot\chromedriver\chromedriver_win32\chromedriver.exe',
                options=options
)

driver.maximize_window()


bot = telebot.TeleBot('5231731574:AAE3d-9mImXvoAElaBvaj2b79egVnZw4x1s')
delay = random.randint(30, 60)
ids = []    # need to transform into set before sending
start_url = 'hui'

@bot.message_handler(commands=['start'])
def start_message(message):
    global ids, start_url
    id = message.from_user.id
    ids.append(id)
    bot.send_message(id, 'Начался мониторинг объявлений!')

    try:
        driver.get('https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5')
        soup = BeautifulSoup(driver.page_source, 'lxml')

        urls = [url.find('td', class_='photo-cell').find('a')['href'] for url in soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
        start_url = urls[0]
        bot.send_message(id, start_url)
    except Exception as ex:
        print(ex)
        bot.send_message(id, 'Мониторинг уже начат')
    finally:
        driver.close()
        driver.quit()



def send_reminder():
    global ids, start_url
    print(start_url)
    try:
        driver.get('https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5')
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        urls = [url.find('td', class_='photo-cell').find('a')['href'] for url in soup.find('table', {'id': 'offers_table'}).find_all('tr', class_='wrap')]
        unprocessed_urls = []
        for url in urls:
            if url == start_url:
                break
            else:
                unprocessed_urls.append(url)

    except Exception as ex:
        print(ex)
        unprocessed_urls = []

    try:
        while True:
            for id in ids:
                for url in unprocessed_urls:
                    bot.send_message(id, f'<a href="{url}">Найдена новая ссылка</a>', parse_mode='HTML')
            time.sleep(delay)

    except Exception as ex:
        print(ex)

t = threading.Thread(target=send_reminder)
t.start()

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        time.sleep(10)