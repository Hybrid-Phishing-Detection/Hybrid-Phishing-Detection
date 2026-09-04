# File: backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# LightGBM 구동에 필요한 libgomp1 시스템 패키지 설치
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]