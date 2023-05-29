import requests
import random
import os
from datetime import datetime
import calendar

import telegram
import asyncio

from config import CONFIG


def get_content(index: int):
    current_dir = os.getcwd()
    content_path = os.path.join(current_dir, 'logwork', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def alert_logwork(index: int):
    content = get_content(index)
    params = {'chat_id': CONFIG.get('group_id'), 'text': content, 'parse_mode': 'markdown'}
    bot_token = CONFIG.get('bot_token')
    req = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=params)


if __name__ == '__main__':
    today = datetime.today()
    last_day_of_month = calendar.monthrange(today.year, today.month)
    if today.day == last_day_of_month:
        content_index = 'last'
    else:
        content_index = random.randint(1, 2)
    alert_logwork(content_index)
