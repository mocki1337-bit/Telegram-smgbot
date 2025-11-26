FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/ .

FROM gcc:latest AS backend-build
WORKDIR /app/backend
COPY backend/ .
RUN apt-get update && apt-get install -y cmake
RUN cmake . && make

FROM ubuntu:22.04
WORKDIR /app


COPY --from=backend-build /app/backend/authsrv /app/backend/
COPY --from=frontend-build /app/frontend /app/frontend/

RUN apt-get update && apt-get install -y \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["/app/backend/authsrv"]

