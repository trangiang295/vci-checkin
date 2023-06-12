import requests
import random
import os
import math
from datetime import datetime

import telegram
import asyncio

from config import CONFIG
from constant import SPLIT_TXT, TELE_LINE_NUM
from utilities.weather import WeatherAPI


def get_content(index: int):
    current_dir = os.getcwd()
    content_path = os.path.join(current_dir, 'content', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def make_line_with_space(sentences: list):
    sentences_len = [len(x) for x in sentences]
    space_len = math.floor((TELE_LINE_NUM - sum(sentences_len)) / (len(sentences) - 1))
    space = int(space_len * 2) * ' '
    return space.join(sentences) + '\n'


def rain_or_sun_emoji(description: str, is_morning: bool or None):
    if "mưa" in description.lower():
        if is_morning is None:
            note = ''
        else:
            note = '  🔜  *Đi sớm*' if is_morning else '*Về sớm*'
        return f'☔☔☔{note}'
    elif "nắng" in description.lower():
        return '🌞🌞🌞'
    elif "mây" in description.lower():
        return '☁☁☁'
    else:
        return ''


def query_weather_info():
    content = ''
    try:
        weather_api = WeatherAPI(CONFIG['weatherapi_token'])
        utc_hour = datetime.utcnow().hour
        if utc_hour < 5:
            data = weather_api.forecast_afternoon_today()
            content += '`Hôm nay:`\n'
            elements = [
                f"🌡️: {data['today']['temp']}°C",
                f"💦: {data['today']['humidity']}%",
                f"UV: {data['today']['uv']}"
            ]
            content += make_line_with_space(elements)
            description = data['today']['description']
            content += f"Khả năng mưa: {data['today']['chance_of_rain']}%\n" \
                       f"*{description}*     {rain_or_sun_emoji(description, None)}\n{SPLIT_TXT}"
            ##################################################
            content += '`17h chiều nay:`\n'
            elements = [
                f"🌡️: {data['forecast_5pm']['temp']}°C",
                f"💦: {data['forecast_5pm']['humidity']}%",
                f"UV: {data['forecast_5pm']['uv']}"
            ]
            content += make_line_with_space(elements)
            elements = [
                f"Khả năng mưa: {data['forecast_5pm']['chance_of_rain']}%",
                f"Cảm giác như: {data['forecast_5pm']['feelslike']}°C",
            ]
            content += make_line_with_space(elements)
            description = data['forecast_5pm']['description']
            content += f"*{description}*     {rain_or_sun_emoji(description, False)}"
        else:
            data = weather_api.forecast_morning_tomorrow()
            content += '`Hôm nay:`\n'
            elements = [
                f"🌡️: {data['today']['temp']}°C",
                f"💦: {data['today']['humidity']}%",
                f"UV: {data['today']['uv']}"
            ]
            content += make_line_with_space(elements)
            description = data['today']['description']
            content += f"Khả năng mưa: {data['today']['chance_of_rain']}%\n" \
                       f"*{description}*     {rain_or_sun_emoji(description, None)}\n{SPLIT_TXT}"
            ####################################################
            content += '`7h sáng mai:`\n'
            elements = [
                f"🌡️: {data['forecast_7am']['temp']}°C",
                f"💦: {data['forecast_7am']['humidity']}%",
                f"UV: {data['forecast_7am']['uv']}"
            ]
            content += make_line_with_space(elements)
            elements = [
                f"Khả năng mưa: {data['forecast_7am']['chance_of_rain']}%",
                f"Cảm giác như: {data['forecast_7am']['feelslike']}°C",
            ]
            content += make_line_with_space(elements)
            description = data['forecast_7am']['description']
            content += f"*{description}*     {rain_or_sun_emoji(description, True)}\n{SPLIT_TXT}"
            ######################################################
            content += '`Cả ngày mai:`\n'
            elements = [
                f"🌡️: {data['forecast_day']['temp']}°C",
                f"💦: {data['forecast_day']['humidity']}%",
                f"UV: {data['forecast_day']['uv']}"
            ]
            content += make_line_with_space(elements)
            description = data['forecast_day']['description']
            content += f"Khả năng mưa: {data['forecast_day']['chance_of_rain']}%\n" \
                       f"*{description}*     {rain_or_sun_emoji(description, None)}"
        return content
    except:
        return ''


def alert_diemdanh(index: int):
    content = get_content(index)
    weather_content = query_weather_info()
    content += '\n' + SPLIT_TXT + weather_content
    params = {'chat_id': CONFIG.get('group_id'), 'text': content, 'parse_mode': 'markdown'}
    bot_token = CONFIG.get('bot_token')
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=params)


async def test():
    bot = telegram.Bot(CONFIG.get('bot_token'))
    async with bot:
        print(await bot.get_updates())

if __name__ == '__main__':
    content_index = random.randint(1, 1)
    alert_diemdanh(content_index)
    # asyncio.run(test())
