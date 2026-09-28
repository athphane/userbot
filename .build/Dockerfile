# Stage 1: Build
FROM python:3.11-slim-bookworm AS build

WORKDIR /root/userbot

COPY . .

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && \
    apt-get install -y gcc build-essential --no-install-recommends && \
    python -m pip install --upgrade pip==26.2.1 && \
    python -m pip install -r requirements.txt && \
    apt-get autoremove -y gcc build-essential && \
    apt-get clean

# Stage 2: Run
FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.source https://github.com/athphane/userbot
LABEL org.opencontainers.image.description "Telegram Userbot Container Image"
LABEL org.opencontainers.image.licenses GPL-3.0

WORKDIR /root/userbot

# COPY merges directories, so remove base packages to avoid retaining older
# distribution metadata and modules alongside the patched build packages.
RUN rm -rf /usr/local/lib/python3.11/site-packages

COPY --from=build /root/userbot .
COPY --from=build /usr/local /usr/local

CMD python -m userbot
