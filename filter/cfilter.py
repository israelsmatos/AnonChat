from aiogram import filters
from aiogram.types import Message, CallbackQuery
from config import banned_users, admin, banned_users_file
from json import dumps, loads

class Admin(filters.Filter):
    async def __call__(self, msg):
        if type(msg) == CallbackQuery:
            print("Yes its callback")
            msg = msg.message

        if msg.chat.id in admin:
            return True
        return False

class Banned(filters.Filter):
    def __init__(self):
        self.banned_users = banned_users

    def add(self, userid):
        banned_users.append(userid)
        print(f"BANNED: Successfully added {userid}")

    def pop(self, userid):
        if userid in banned_users:
            banned_users.pop(banned_users.index(userid))
        self.save_file()
        print(f"NOT BANNED: Successfully removed {userid}")

    async def __call__(self, msg):
        if type(msg) == CallbackQuery:
           userid = msg.message.from_user.id
        else:
            userid = msg.chat.id

        print(userid, type(userid))
        if userid in banned_users:
            print("Is banned")
            return False
        return True
