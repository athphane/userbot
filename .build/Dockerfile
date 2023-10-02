# Stage 1: Build
FROM python:3.11.5-slim-bullseye AS build

WORKDIR /root/userbot

COPY . .

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && \
    apt-get install -y gcc build-essential --no-install-recommends && \
    pip install -r requirements.txt && \
    apt-get autoremove -y gcc build-essential && \
    apt-get clean

# Stage 2: Run
FROM python:3.11.5-slim-bullseye

WORKDIR /root/userbot

COPY --from=build /root/userbot .
COPY --from=build /usr/local /usr/local
COPY .build/setup /usr/local/bin/setup

RUN chmod +x /usr/local/bin/setup

CMD python -m userbot