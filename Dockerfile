FROM python:3.7-slim-bullseye

RUN apt-get update && apt-get install -y git python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/server.py", "serve"]
