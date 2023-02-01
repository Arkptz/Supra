from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import traceback
from .bot import dp
from multiprocessing import Process
import multiprocessing as mp
from main import Supra, csv, excel_file
from data_class import data_cl


@dp.callback_query_handler(Text(startswith='check_account_'))
async def account_1lvl_menu(cq: CallbackQuery, state: FSMContext):
    print('start proc...')
    msg = cq.message
    user_id = msg.chat.id
    acc = cq.data.split('check_account_')[1]
    data = data_cl(acc)
    data.check = True
    Process(target=Supra(data=data, Lock=mp.Lock() ,csv=csv, excel_file=excel_file).start, ).start()