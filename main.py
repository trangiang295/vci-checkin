import requests
import random
import os
from datetime import datetime

import telegram
import asyncio

from config import CONFIG


def get_content(index: int):
    content_path = os.path.join('content', f'{index}.txt')
    f = open(content_path, 'r', encoding='utf-8')
    return f.read()


def alert_diemdanh(index: int):
    content = get_content(index)
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
