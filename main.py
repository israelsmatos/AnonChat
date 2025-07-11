from aiogram import Bot, Dispatcher, exceptions, Router, filters
from aiogram.client import default
from aiogram.types import *
from pathlib import Path

#from src.utils import generate_buttons
from src.gnbtn import gen_btn
from src.database import Users
from src.langloader import Langloader
from src.sessionloader import SessionLoader
from config import token, LANG, ANON, USERNAME, LOGGED, default_lang, banned_users

from random import choice

r = Router(name="router")
local = Path().resolve()
langs = Langloader()
session = SessionLoader()
lang_dict = langs()


# TODO implement a queue for available users 1st-in/1st-out
async def check_queue():
    if len(session.queue) % 2 == 0:
        for ids in session.users:
            if session.users[ids][ANON] == 0:
                if ids != session.queue[0]:
                    session.users[ids][ANON] = session.queue[0]
                    session.users[session.queue[0]][ANON] = ids
                    await main.send_message(ids, lang_dict[session.users[ids][LANG]][check_queue.__name__]['t1'].format(session.users[session.queue[0]][USERNAME]))
                    await main.send_message(session.queue[0], lang_dict[session.users[ids][LANG]][check_queue.__name__]['t1'].format(session.users[ids][USERNAME]))
                    session.queue.pop(session.queue.index(session.users[ids][ANON]))
                    session.queue.pop(session.queue.index(ids))

@r.callback_query(session.Banned())
async def callback(q: CallbackQuery):
    msg = q.message
    data = q.data

    if data in langs.available_langs:
        session.users[msg.chat.id] = {LOGGED: False, USERNAME: "", ANON: 0, LANG: data}
        btn = gen_btn([lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['b2']], ["c"])
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][start.__name__]['t2'], reply_markup=btn)
        await main.edit_message_text(lang_dict[session.users[msg.chat.id][LANG]][callback.__name__]['t1'].format(session.users[msg.chat.id][LANG]), msg.chat.id, msg.message_id)
    
    if data == "c" or session.users[msg.chat.id][USERNAME] == 0 and data == "c":
        username = choice(session.usernames)
        session.queue.append(msg.chat.id)
        if not session.users[msg.chat.id][LOGGED]:
            session.users[msg.chat.id][LOGGED] = True
            session.users[msg.chat.id][USERNAME] = username
        
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][callback.__name__]['t2'])
        
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][callback.__name__]['t3'].format(session.users[msg.chat.id][USERNAME]))
        session.usernames.pop(session.usernames.index(username))
        await check_queue()
    
    elif session.users[msg.chat.id][LOGGED] and session.users[msg.chat.id][ANON] == 0:
        session.queue.append(msg.chat.id)
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][callback.__name__]['t2'])
        
        #reuse t1 and t2
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][callback.__name__]['t3'].format(session.users[msg.chat.id][USERNAME]))
        await check_queue()

@r.message(session.Banned() and filters.Command("finish")) #and Banned())
async def finish(msg: Message):
    if session.users[msg.chat.id][ANON] != 0:
        btn = gen_btn([lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['b1']], ["c"])
        await main.send_message(session.users[msg.chat.id][ANON], lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['t1'].format(session.users[msg.chat.id][USERNAME]), reply_markup=btn)
        session.users[session.users[msg.chat.id][ANON]][ANON] = 0
    
    session.users[msg.chat.id][USERNAME] = ""
    session.users[msg.chat.id][LOGGED] = False

    btn = gen_btn([lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['b2']], ["c"])
    await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['t2'], reply_markup=btn)
    try :session.queue.pop(session.queue.index(msg.chat.id))
    except: pass


@r.message(session.Banned() and filters.Command("end"))
async def end_chat(msg: Message):
    btn = gen_btn([lang_dict[session.users[msg.chat.id][LANG]][finish.__name__]['b1']], ["c"])
    await main.send_message(session.users[msg.chat.id][ANON], lang_dict[session.users[msg.chat.id][LANG]][end_chat.__name__]['t1'].format(session.users[msg.chat.id][USERNAME]), reply_markup=btn)
    
    await main.send_message(session.users[session.users[msg.chat.id][ANON]][ANON], lang_dict[session.users[msg.chat.id][LANG]][end_chat.__name__]['t2'], reply_markup=btn)
    session.users[session.users[msg.chat.id][ANON]][ANON] = 0    
    session.users[msg.chat.id][ANON] = 0
    
    
@r.message(session.Banned())
async def start(msg: Message):
    # db_id, id, name, username, chat_with, message
    data = {
        'id': msg.chat.id,
        'name': msg.from_user.first_name,
        'username': msg.chat.username,
        'chat_with': "bot",
        'message': msg.text,
        'lang': "en-us"
    }

    if msg.chat.id not in session.users:
        session.users[msg.chat.id] = {LOGGED: False, USERNAME: "", ANON: 0, LANG: "en-us"}
        btns = gen_btn([m for m in langs.available_langs], [m for m in langs.available_langs])
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][start.__name__]['t1'], reply_markup=btns)
        Users().save_data(data)

    if msg.chat.id in session.users and session.users[msg.chat.id][LOGGED] == False:
        btn = gen_btn(["Chat now!"], ["c"])
        await main.send_message(msg.chat.id, lang_dict[session.users[msg.chat.id][LANG]][start.__name__]['t2'], reply_markup=btn)
    
    elif session.users[msg.chat.id][LOGGED] and not session.users[msg.chat.id][LOGGED] == KeyError:
        data['chat_with'] = session.users[msg.chat.id][ANON]
        data['message'] = msg.text
        Users().save_data(data)
        await main.send_message(session.users[msg.chat.id][ANON], lang_dict[session.users[msg.chat.id][LANG]][start.__name__]['t3'].format(session.users[msg.chat.id][USERNAME], msg.text))

@r.message(filters.Command("ban") and session.Admin())
async def ban(msg: Message):
    if int(msg.text.split(sep=" ")[1]):
        user = int(msg.text.split(sep=" ")[1])
        session.Banned().add(user)


#@r.message(Admin() and filters.Command("unban"))
async def unban(msg: Message):
    ...
       

@r.shutdown()
@r.message(filters.Command("shutdown") and session.Admin())
async def shutdown():
    print("Emergency shutdown initiated...")
    Users().close()
    session.finish()


if __name__ == "__main__":
    session.init()
    Users().initialise()
    print(f'Available languages: {[i for i in langs.available_langs]}')
    print(f"Available usernames: {len(session.usernames)}")
    print(f"Banned users: {len(session.banned_users)}")
    
    main = Bot(token, default=default.DefaultBotProperties(parse_mode='HTML', protect_content=True))
    d = Dispatcher()
    d.include_router(r)
    d.run_polling(main, skip_updates=True, handle_signals=True)
