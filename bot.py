import telebot
from telebot.types import InputMediaPhoto
import time
from selenium_part import OlxParser
import random
import os

BOT_TOKEN = '5231731574:AAE3d-9mImXvoAElaBvaj2b79egVnZw4x1s'
CHANNEL_NAME = '@olx_scraper'
OLX_URL = 'https://www.olx.ua/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5'
# start_url = 'https://www.olx.ua/d/uk/obyavlenie/arenda-kvartiry-do-10000-IDOhg4R.html#000d3b0210'

bot = telebot.TeleBot(BOT_TOKEN)
last_id = '742960032'

while True:
    result = OlxParser('https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/chernovtsy/?search%5Bdist%5D=5', last_id).get()

    if result:
        last_id, data_list = result
        print(last_id)

        for data in data_list:
            if data['photosList']:
                media_group = []
                caption = f'<a href="{data["url"]}">{data["title"]}</a>\n' \
                          f'\n' \
                          f'<b>Ціна:</b> {data["price"]}\n' \
                          f'<b>Автор:</b> {data["author"]}\n' \
                          f'<b>Номер телефону:</b> {data["phoneNumber"] if data["phoneNumber"] else "<i>не вдалося отримати</i>"}\n'

                for num, photo in enumerate(data['photosList'][:8]):
                    media_group.append(InputMediaPhoto(photo, caption=caption if num == 0 else '', parse_mode='html'))

                try:
                    bot.send_media_group(chat_id=CHANNEL_NAME, media=media_group)
                except Exception as ex:
                    time.sleep(60)
                    bot.send_media_group(chat_id=CHANNEL_NAME, media=media_group)


                time.sleep(10)
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

                time.sleep(4)

        time.sleep(random.randint(60, 210))
