FROM python:3.11-slim-bookworm

WORKDIR /root/userbot

COPY requirements.txt .

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && \
    apt-get install -y gcc build-essential --no-install-recommends && \
    python -m pip install --upgrade pip==26.2.1 && \
    python -m pip install -r requirements.txt && \
    apt-get autoremove -y gcc build-essential && \
    apt-get clean

CMD python -m userbot
