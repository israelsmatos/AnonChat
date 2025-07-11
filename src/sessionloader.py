from pathlib import Path
from json import dumps, loads
from aiogram import filters
from aiogram.types import Message, CallbackQuery

from config import banned_users, users_json, admin, usernames

class SessionLoader:
    def __init__(self, users={}, queue=[], username_path=""):
        self.banned_users = banned_users
        self.users = users
        self.queue = queue
        self.usernames = []
    
    def _string_to_userid_list(self, string:str) -> list:
        re = ""
        result = []
        for item in string:
            if item not in list('[], "'):
                re = re + item

            if len(re) == 10:
                result.append(int(re))
                re = ""
        
        return result
    
    def init(self):
        with open("snapshot.json", "r") as big:
            data = loads(big.read())
            for key in data['users']:
                self.users[int(key)] = data['users'][key]
            
            self.queue = self._string_to_userid_list(data['queue'])
            self.banned_users = self._string_to_userid_list(data['banned_users'])

        with open(usernames, "r") as u:
            self.usernames = [i.replace("\n", "") for i in u]

    
    def finish(self):
        with open("snapshot.json", "w") as big:
            data = {
                "users": self.users,
                "queue": self.queue,
                "banned_users": self.banned_users,
            }
            big.write(dumps(data))
        with open(users_json) as f:
            f.write(dumps(self.users, indent=4))
        print("Saved bot snapshot.")

    def __repr__(self):
        return f"""
Session Data:
usernames: {self.usernames}
banned: {self.banned_users}
users: {self.users}
queue: {self.queue}
        """


# Filters
    class Admin(filters.Filter):
        async def __call__(self, msg):
            if type(msg) == CallbackQuery:
                print("Yes its callback")
                msg = msg.message
                self

            if msg.chat.id in admin:
                return True
            return False

    class Banned(filters.Filter):
        def add(self, userid):
            SessionLoader().banned_users.append(userid)
            print(f"BANNED: Successfully added {userid}")

        def pop(self, userid):
            if userid in SessionLoader().banned_users:
                SessionLoader().banned_users.pop(SessionLoader().banned_users.index(userid))
            print(f"NOT BANNED: Successfully removed {userid}")

        async def __call__(self, msg):
            if type(msg) == CallbackQuery:
                userid = msg.message.from_user.id
            else:
                userid = msg.chat.id

            if userid in SessionLoader().banned_users:
                print("Is banned")
                return False
            return True