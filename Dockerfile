FROM python:3.10-slim

ENV LANG=C.UTF-8

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sqlite3 curl && \
    apt-get clean

WORKDIR /rest-api-py

COPY . /rest-api-py

EXPOSE 8080

CMD ["python3", "main.py"]