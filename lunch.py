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
    content_path = os.path.join(current_dir, 'lunch', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def alert_lunch(index: int):
    content = get_content(index)
    params = {'chat_id': CONFIG.get('fresher_group_id'), 'text': content, 'parse_mode': 'markdown'}
    bot_token = CONFIG.get('bot_token')
    api_url = CONFIG.get("api_url", "api.telegram.org")
    req = requests.post(f'https://{api_url}/bot{bot_token}/sendMessage', data=params)


if __name__ == '__main__':
    content_index = random.randint(1, 1)
    if is_holiday():
        pass
    else:
        alert_lunch(content_index)
