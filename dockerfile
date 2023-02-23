FROM python:3.10.4-slim-buster as python

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN flask --app src.adapters.app.application init-db

EXPOSE 8000

CMD [ "flask", "--app", "src.adapters.app.application", "--debug", "run", "-h", "0.0.0.0", "-p", "8000"]