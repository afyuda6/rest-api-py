FROM python:3.10-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /rest-api-py

COPY . /rest-api-py

EXPOSE 8080

CMD ["python3", "main.py"]