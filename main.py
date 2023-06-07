import requests
import random
import os
from datetime import datetime

import telegram
import asyncio

from config import CONFIG
from constant import SPLIT_TXT
from utilities.weather import WeatherAPI


def get_content(index: int):
    current_dir = os.getcwd()
    content_path = os.path.join(current_dir, 'content', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def query_wheather_info():
    try:
        weather_api = WeatherAPI(CONFIG['weatherapi_token'])
        utc_hour = datetime.utcnow().hour
        if utc_hour < 5:
            data = weather_api.forecast_afternoon_today()
        else:
            data = weather_api.forecast_morning_tomorrow()
        return f'{data}'
    except:
        return ''


def alert_diemdanh(index: int):
    content = get_content(index)
    weather_content = query_wheather_info()
    content += SPLIT_TXT + weather_content
    params = {'chat_id': CONFIG.get('group_id'), 'text': content}
    bot_token = CONFIG.get('bot_token')
    req = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=params)


async def test():
    bot = telegram.Bot(CONFIG.get('bot_token'))
    async with bot:
        print(await bot.get_updates())

if __name__ == '__main__':
    content_index = random.randint(1, 1)
    alert_diemdanh(content_index)
    # asyncio.run(test())
