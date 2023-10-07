import sqlite3

from config import db_directory, db_name


async def query_to_db(query: str):
    """ Create a database connection, executes a query, and close the connection

    :param query:
    :return status/exception:
    """

    # Create connection and cursor
    connection = sqlite3.connect(db_directory + db_name)
    cursor = connection.cursor()

    # Catch Exceptions
    try:
        # Make a request to the database
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as error:
        return error

    # Close connection
    connection.close()
    return 'OK'


async def get_values_from_db(query: str):
    """ Create a database connection, executes a query, return data and close the connection

    :param query:
    :return data/exception:
    """
    # Create connection and cursor
    connection = sqlite3.connect(db_directory + db_name)
    cursor = connection.cursor()

    # Catch Exceptions
    try:
        # Make a request to the database
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as error:
        return error

    # Close connection and return data
    connection.close()
    return result


async def get_user_from_db(column: str, user_data: str) -> str:
    """ Retrieves data from the database and checks for the specified parameters

    :param column:
    :param user_data:
    :return status/exception:
    """
    query = f'SELECT * FROM users WHERE {column} = "{user_data}"'
    user_data = await get_values_from_db(query=query)

    if type(user_data) is sqlite3.OperationalError:
        return 'sqlite3.error' + str(user_data)

    elif len(user_data) == 0:
        return 'OK'

    elif len(user_data) != 0:
        return 'The user is already exist'


async def insert_new_user(user_email: str, user_id: str, hashed_password: str, salt: str):
    """ Add new user to database

    :param user_email:
    :param user_id:
    :param hashed_password:
    :param salt:
    :return status/exception:
    """
    query = f'''
    INSERT INTO 
        users (user_email, user_id, password, salt)
    VALUES
        ("{user_email}", "{user_id}", "{hashed_password}", "{salt}")
    '''
    return await query_to_db(query=query)

