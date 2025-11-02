FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
