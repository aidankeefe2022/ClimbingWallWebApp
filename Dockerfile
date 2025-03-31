FROM ubuntu:latest
LABEL authors="aidan"

ENTRYPOINT ["top", "-b"]

COPY . .

RUN apt -y update && apt install -y sqlite3

RUN sqlite3 --version

CMD["python3", "app.py"]