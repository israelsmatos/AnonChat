#Bot configs
admin = [] # set admins here(account id)
banned_users = []
token = "" # Account token
LANG = "lang"
ANON = 'anon'
LOGGED = 'logged'
USERNAME = 'username'
default_lang = 'en-us'


# dirs & essential files
assets_dir = "assets/"
lang_dir = "lang/"
db_dir = "db/"
usernames = 'assets/usernames.txt'
users_json = 'users-data.json'
banned_users_file = "assets/banned.txt"


#Database configs
dbname = "anonrc"
# db_id, id, name, username, chat_with, message
user_tables = "db_id INTEGER PRIMARY KEY AUTOINCREMENT, lang TEXT NOT NULL, id INTEGER NOT NULL, name TEXT NOT NULL, username TEXT NOT NULL, message TEXT"
message_tables = ""
USERS = 'users'
table_layouts = {
    USERS: user_tables
}
check_data_table = "SELECT {} FROM {} WHERE"
init_table = "CREATE TABLE IF NOT EXISTS '{}' ({})"
insert_data = "INSERT INTO '{}' VALUES (NULL, {})"
update_data = "UPDATE '{}' SET {} WHERE {}"
fetch_data_condition = "SELECT {} FROM {} WHERE {};"
fetch_data = "SELECT {} FROM '{}'"
delete_data = "DELETE FROM '{}' WHERE {}"
drop_table = "DROP TABLE '{}'"
