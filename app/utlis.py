import string
import random
import hashlib

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database import insert_new_user
from config import smtp_data


async def add_and_send_user_data(user_email: str, user_id: str) -> str:
    """ Accept email and UUID, then generate password and hashed password, after send message to the email

    :param user_email:
    :param user_id:
    :return status/exception:
    """

    # Generate new password
    password = await generate_new_password()

    # Generate hashed password
    hashed_password, salt = await new_hash_password(password=password)

    # Send message to email
    status = await send_message(receiver_email=user_email, password=password, user_id=user_id)

    if status != 'OK':
        return status

    # Add data in database
    add_new_user = await insert_new_user(user_email=user_email, user_id=user_id,
                                         hashed_password=hashed_password, salt=salt)

    # Catch Exception
    if add_new_user != 'OK':
        return str(add_new_user)

    return status


async def generate_new_password() -> str:
    """ Generate random password (length = 20)

    :return password:
    """

    # Choose random string/digit and generate random password
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(16))

    # Split the password into groups of 4 characters each and return password
    password_with_separator = '-'.join([password[i:i + 4] for i in range(0, 16, 4)])
    return password_with_separator


async def new_hash_password(password: str) -> tuple:
    """ Hash received password

    :param password:
    :return salt, hashed_password:
    """

    # Generate random salt
    salt = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

    # Concatenate the password and salt
    salted_password = password + '.' + salt

    # Hash the password using the salt
    password_bytes = salted_password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return salt, hashed_password


async def send_message(receiver_email: str, password: str, user_id: str) -> str:
    """ Send message to specified email

    :param receiver_email:
    :param password:
    :param user_id:
    :return status/exception:
    """

    # Set up SMTP data
    smtp_server = smtp_data['server']
    smtp_port = smtp_data['port']
    smtp_username = smtp_data['username']
    smtp_password = smtp_data['password']
    message_text = f'Your user ID: {user_id}\nYour password: {password}'

    # Create MIMEText object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg['Subject'] = 'User data'
    msg.attach(MIMEText(message_text, 'plain'))

    try:

        # Create connection with SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Auth on SMTP
        server.login(smtp_username, smtp_password)

        # Sending message
        server.sendmail(smtp_username, receiver_email, msg.as_string())
        server.quit()
        return 'OK'

    except Exception as error:
        return 'smtp.error:' + str(error)
