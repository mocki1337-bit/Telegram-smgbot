FROM gcc:latest AS backend-build
WORKDIR /app/backend
COPY backend/ .

RUN apt-get update && apt-get install -y \
    cmake \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN cmake . && make

FROM ubuntu:22.04
WORKDIR /app

COPY --from=backend-build /app/backend/authsrv /app/backend/authsrv

COPY frontend/ /app/frontend/

RUN apt-get update && apt-get install -y \
    libcurl4 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["/app/backend/authsrv"]

