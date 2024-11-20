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
    content_path = os.path.join(current_dir, 'lunch', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def alert_lunch(index: int):
    content = get_content(index)
    params = {'chat_id': CONFIG.get('fresher_group_id'), 'text': content, 'parse_mode': 'markdown'}
    bot_token = CONFIG.get('bot_token')
    req = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=params)


if __name__ == '__main__':
    content_index = random.randint(1, 1)
    alert_lunch(content_index)