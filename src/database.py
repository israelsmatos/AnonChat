# A simple DATABASE interface for Atlas
# from aiogram.types import Message
import sqlite3, logging
from config import *

def logs(message: str, level=logging.INFO) -> logging.Logger:
	return logging.log(level, message)

logging.basicConfig(format="[%(asctime)s - %(message)s - %(levelname)s]", level=logging.INFO)

class Database:
    def __init__(self, table_name: str):
        self.dbc = sqlite3.connect(db_dir + dbname)
        self.cur = self.dbc.cursor()
        self.table_name = table_name
        self.parameters = []

        get_parameters = table_layouts[self.table_name].split(sep=",")
        for item in get_parameters:
            self.parameters.append(item.strip().split(sep=" ")[0])
        
        self.parameters
    
    # Commit table layouts
    def initialise(self):
        logs(f"{self.table_name} initialised successfully")
        cmd = init_table.format(self.table_name, table_layouts[self.table_name])
        self.cur.execute(cmd)
        self.dbc.commit()

    
    # Dynamically save data using table keys
    # The keys supplied by the dictionary can be in any order
    def save_data(self, data: dict, is_document=False):
        complement = ""
        parameters = []
        data_id = ""

        get_parameters = table_layouts[self.table_name].split(sep=",")
        for item in get_parameters:
            if not "db_id" in item:
                parameters.append(item.strip().split(sep=" ")[0])
        
        for key in self.parameters:
            if key in data:
                if complement == "":
                    data_id = key
                    complement = complement + f"'{data[key]}'"
                else:
                    complement = complement + f",'{data[key]}'"
            else:
                logs(f"{key} parameter does not exist in table {self.table_name}")

        
        logs(insert_data.format(self.table_name, complement))
        self.cur.execute(insert_data.format(self.table_name, complement))
        self.dbc.commit()

        logs(f"{data[data_id]} saved successfully")

        
        logs(insert_data.format(self.table_name, complement))
        self.cur.execute(insert_data.format(self.table_name, complement))
        self.dbc.commit()

        logs(f"{data_id} saved successfully")
    
        
    def fetch_data(self, table_item, condition: str="", check=False):
        if condition != "":
            cmd = fetch_data_condition.format(table_item, self.table_name, condition)
        else:
            cmd = fetch_data.format(table_item, self.table_name)
        
        self.cur.execute(cmd)
        
        if check:
            if len(self.cur.fetchall()) != 0:
                return True
            return False

        return self.cur.fetchall()
    

    # def save_user(self, msg: Message):
    #     for item in msg:
    #     user = {
    #         "username": msg.chat.username,
    #         "userid": msg.chat.id,
    #         "name": msg.from_user.first_name,
    #         "linked_emails": users[msg.chat.id].user_emails,
    #         "premium": False,
    #         "unix_creation_date": time.time()
    #     }
    #     Users().save_data(user)

    # def check(self, key):
    #     self.cur.execute(check_data_table.format(key, self.table_name, ))

    def delete_data(self, condition: str):
        cmd = delete_data.format(self.table_name, condition)
        self.cur.execute(cmd)
        self.dbc.commit()
        logs("Deleted seccessfully")

    
    def drop_table(self):
        cmd = drop_table.format(self.table_name)
        self.cur.execute(cmd)
        self.dbc.commit()
        logs(f"Table {self.table_name} dropped successfully")
    
    def close(self):
        self.cur.close()
        self.dbc.close()
        logs("All connections closed.")

class Users(Database):
    def __init__(self):
        self.table_name: str = USERS
        super().__init__(self.table_name)
    
    def get_user(self, userid: int) -> bool:
        cmd = f"SELECT * FROM {self.table_name} WHERE id={userid}"
        self.cur.execute(cmd)
        if len(self.cur.fetchall()) != 0:
            return False
        return True

# class Files(Database):
#     def __init__(self):
#         self.table_name: str = FILES
#         super().__init__(self.table_name)
    
#     def get_file(self, url):
#         cmd = f"SELECT file_id, is_media_group from {self.table_name} WHERE url='{url}'"
#         self.cur.execute(cmd)
#         data = self.cur.fetchall()
#         if len(data) != 0:
#             return data
#         return False
