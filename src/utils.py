from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


def generate_buttons(text: list, callback: list=[], side_by_side: bool = False, self_inline: tuple = (False, '')):
    n = len(text)
    keyboard = InlineKeyboardMarkup(row_width=3)
    if side_by_side:
        side_btns = []
        for n in range(0, n):
            btn = InlineKeyboardButton(text[n], callback_data=callback[n],)
            side_btns.append(btn)

        keyboard = InlineKeyboardMarkup(row_width=2, 
                    inline_keyboard=[ side_btns ])
    
    elif self_inline[0]:
        for n in range(0, n):
            if n == text.index(self_inline[1]):
                btn = InlineKeyboardButton(text[n], switch_inline_query_current_chat='')
                keyboard.add(btn)
    
    else:
        for n in range(0, n):
            keyboard.add(InlineKeyboardButton(text=text[n], callback_data=callback[n]))

    
    return keyboard
