#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from pyrogram import Client

APP_ID = int(input("enter Telegram APP ID: "))
API_HASH = input("enter Telegram API HASH: ")


async def main(api_id, api_hash):
    """ generate StringSession for the current MemorySession"""
    async with Client(
            ":memory:",
            api_id=api_id,
            api_hash=api_hash
    ) as app:
        print(app.export_session_string())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(APP_ID, API_HASH))
