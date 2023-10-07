FROM python:3.10.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /databasess

ADD /app /app

RUN python create_db.py

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
