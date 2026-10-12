"""Persist chats whose incoming social links may be downloaded."""

import json
import os

CHATS_PATH = os.path.join("config", "social_dl_chats.json")


def list_chats() -> list[int]:
    """Return the chat IDs explicitly enabled by the owner."""
    try:
        with open(CHATS_PATH, encoding="utf-8") as file:
            values = json.load(file).get("enabled_chats", [])
        return sorted({int(value) for value in values})
    except (OSError, ValueError, TypeError, AttributeError):
        return []


def is_chat_enabled(chat_id: int) -> bool:
    """Check whether incoming links are enabled in a chat."""
    return chat_id in list_chats()


def set_chat_enabled(chat_id: int, enabled: bool) -> bool:
    """Save a chat setting and report whether it changed."""
    chats = set(list_chats())
    if enabled == (chat_id in chats):
        return False
    if enabled:
        chats.add(chat_id)
    else:
        chats.remove(chat_id)
    os.makedirs(os.path.dirname(CHATS_PATH), exist_ok=True)
    path = CHATS_PATH + ".tmp"
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"enabled_chats": sorted(chats)}, file, indent=2)
    os.replace(path, CHATS_PATH)
    return True
