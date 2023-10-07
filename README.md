# UUID and Password generator

## Receives an email as input, then generates a password and an UUID, and sends it to the specified email.

## Docs
http://127.0.0.1:8000/docs

- **POST** `/image`
Receives an email, checks for uniqueness, generates a password and UUID, hashes the password, records it in the database, and then sends an email.
Returns JSON `{'status': <DONE/ERROR>, 'details': <details>}`

- **GET** `/health`
Server check

## How to run?
- Fill env.txt

Using docker container
```
docker build . -t uuidgen:latest
cd ./app
python3 create_db.py
docker run -p 127.0.0.1:8000:8000 --env-file=env.txt -v /path/to/directory/app/databases:/app/databases --name=PROD -d uuidgen:latest
```
