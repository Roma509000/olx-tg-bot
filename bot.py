import telebot
import time
from scraper import OlxScraper
import random

BOT_TOKEN = '5231731574:AAE3d-9mImXvoAElaBvaj2b79egVnZw4x1s'
CHANNEL_NAME = '@olx_scraper'
OLX_URL = 'https://www.olx.ua/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5'
start_url = 'https://www.olx.ua/d/uk/obyavlenie/arenda-kvartiry-do-10000-IDOhg4R.html#000d3b0210'

bot = telebot.TeleBot(BOT_TOKEN)

while True:
    start_url, data = OlxScraper().check_general_announcement(OLX_URL, start_url)
    time.sleep(random.randint(30, 60))




