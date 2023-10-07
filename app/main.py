import uuid

from validate_email_address import validate_email
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

from database import get_user_from_db
from utlis import add_and_send_user_data
from models import Email


app = FastAPI()


@app.get('/health')
async def health():
    """
    Server check
    """

    return Response("I'm alive!")


@app.post('/register_user')
async def register_user(user_email: Email):
    """Receives an email, generates a password and id, then sends it to the specified email

           Args:\n
               email (str): Accept email

           Returns:\n
               status, details (JSONResponse): Return status
           """

    # Validate email
    user_email = user_email.email.lower()
    if not validate_email(user_email):
        return JSONResponse({'status': 'ERROR', 'details': f'Email {user_email} is not valid'})

    # Checks if the email is in the database
    is_user_exist = await get_user_from_db(column='user_email', user_data=user_email)
    if is_user_exist == 'OK':

        # Generate UUID
        while True:
            user_id = uuid.uuid4().hex
            check_id = await get_user_from_db(column='user_id', user_data=user_id)
            if check_id == 'OK':
                break

        # Add a new email to the database and send a message to the email
        result = await add_and_send_user_data(user_email=user_email, user_id=user_id)

        # Return status and details
        if result == 'OK':
            return JSONResponse({'status': 'DONE', 'user_id': user_id})
        else:
            return JSONResponse({'status': 'ERROR', 'details': result})
    else:
        return JSONResponse({'status': 'ERROR', 'details': is_user_exist})
