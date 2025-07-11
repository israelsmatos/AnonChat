from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from config import tok
from src.utils import generate_buttons

async def start(msg: Message):
    btn = generate_buttons(["Lol"], ['lulz'])
    await main.send_message(msg.chat.id, "Hey!", reply_markup=btn, message_auto_delete_time=3)

def register(d: Dispatcher):
    d.register_message_handler(start)

main = Bot(tok)
d = Dispatcher(main)
register(d)
executor.start_polling(d, skip_updates=True)
