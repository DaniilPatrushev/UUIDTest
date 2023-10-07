import sqlite3

create_user_db = '''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_email TEXT NOT NULL,
user_id TEXT NOT NULL,
password TEXT NOT NULL,
salt TEXT NOT NULL
);
'''

connection_users = sqlite3.connect('databases/users.db')

cursor_users = connection_users.cursor()
cursor_users.execute(create_user_db)
connection_users.commit()
connection_users.close()
