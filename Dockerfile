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
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY backend/ ./backend/


COPY frontend/ ./frontend/


WORKDIR /app/backend

RUN cmake -S . -B build \
    && cmake --build build --config Release -- -j$(nproc)

EXPOSE 8080

CMD ["/app/backend/build/authsrv"]
