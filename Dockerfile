FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    ca-certificates \
    libcurl4-openssl-dev \
    libssl-dev \
    libsqlite3-dev \
    nlohmann-json3-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем весь проект
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY bot/ ./bot/


WORKDIR /app/backend
RUN cmake -S . -B build \
    && cmake --build build --config Release -- -j$(nproc)


WORKDIR /app/bot
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app

EXPOSE 5000


CMD ["python3", "bot/bot.py"]
