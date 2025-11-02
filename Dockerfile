FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache postgresql-libs postgresql-dev gcc musl-dev


RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
