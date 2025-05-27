import requests
import random
import os
from datetime import datetime
import calendar

import telegram
import asyncio

from config import CONFIG
from utilities.holiday import is_holiday


def get_content(index: int):
    current_dir = os.getcwd()
    content_path = os.path.join(current_dir, 'logwork', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def alert_logwork(index: int):
    content = get_content(index)
    params = {'chat_id': CONFIG.get('group_id'), 'text': content, 'parse_mode': 'markdown'}
    bot_token = CONFIG.get('bot_token')
    api_url = CONFIG.get("api_url", "api.telegram.org")
    req = requests.post(f'https://{api_url}/bot{bot_token}/sendMessage', data=params)


if __name__ == '__main__':
    today = datetime.today()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    if today.day == last_day_of_month:
        content_index = 'last'
    else:
        content_index = random.randint(1, 3)
    if is_holiday():
        pass
    else:
        alert_logwork(content_index)
