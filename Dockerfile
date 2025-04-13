FROM python:3.10.14-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY .env .

CMD ["fastapi","run", "./app/main.py"]
# Expose the port the app runs on   
EXPOSE 8000