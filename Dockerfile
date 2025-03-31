FROM python:3.10-slim
LABEL authors="aidan"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["flask", "run"]