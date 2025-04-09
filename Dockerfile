FROM python:3.10-slim
LABEL authors="aidan"

WORKDIR /app

ENV FLASK_APP=app.py
EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .



CMD ["flask", "run", "--host=0.0.0.0:5000"]