import os

db_directory = './databases/'
db_name = 'users.db'
smtp_data = {
    'server': os.getenv('SMTP_SERVER'),
    'port': os.getenv('PORT'),
    'username': os.getenv('USERNAME'),
    'password': os.getenv('SMTP_PASSWORD')
}

