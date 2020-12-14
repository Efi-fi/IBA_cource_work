import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging


logging.basicConfig(level=logging.DEBUG)
load_dotenv()

bot = Bot(token=str(os.getenv('BOT_TOKEN')))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)



# rd = AutoRedis(host=os.getenv('RD_HOST'),
#                port=os.getenv('RD_PORT'),
#                password=os.getenv('RD_PASSWORD'),
#                socket_connect_timeout=1)
# ps = PostgreSQL(database=os.getenv('PS_NAME'),
#                 user=os.getenv('PS_USER'),
#                 password=os.getenv('PS_PASSWORD'),
#                 host=os.getenv('PS_HOST'),
#                 port=os.getenv('PS_PORT'))
