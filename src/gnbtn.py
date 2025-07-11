from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_btn(text: list, callback: list):
    n = len(text)
    btns = []
    a = []
    for n in range(0, n):
        btns.append(InlineKeyboardButton(text=text[n], callback_data=callback[n]))
    a.append(btns)
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=a)
