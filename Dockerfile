FROM ubuntu:latest
LABEL authors="aidan"

ENTRYPOINT ["top", "-b"]

COPY . .

RUN apt update && apt install -y sqlite3

RUN sqlite3 --version