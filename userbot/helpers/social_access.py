"""Persistent access list for private social media downloads."""

import json
import os

ALLOWLIST_PATH = os.path.join("config", "social_dl_allowlist.json")


def list_users() -> list[int]:
    """Read allowed Telegram user IDs from disk."""
    try:
        with open(ALLOWLIST_PATH, encoding="utf-8") as file:
            values = json.load(file).get("allowed_users", [])
        return sorted({int(value) for value in values})
    except (OSError, ValueError, TypeError, AttributeError):
        return []


def _save(users: set[int]) -> None:
    """Persist the allowed users."""
    os.makedirs(os.path.dirname(ALLOWLIST_PATH), exist_ok=True)
    path = ALLOWLIST_PATH + ".tmp"
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"allowed_users": sorted(users)}, file, indent=2)
    os.replace(path, ALLOWLIST_PATH)


def add_user(user_id: int) -> bool:
    """Add an ID and report whether it was new."""
    users = set(list_users())
    if user_id in users:
        return False
    users.add(user_id)
    _save(users)
    return True


def remove_user(user_id: int) -> bool:
    """Remove an ID and report whether it was present."""
    users = set(list_users())
    if user_id not in users:
        return False
    users.remove(user_id)
    _save(users)
    return True


async def is_user_allowed(bot, user_id: int, owner_id: int, group_id: int) -> bool:
    """Grant access to the owner, listed users, and group members."""
    if user_id == owner_id or user_id in list_users():
        return True
    if group_id:
        try:
            member = await bot.get_chat_member(group_id, user_id)
            return str(member.status).lower().split(".")[-1] in {
                "member", "administrator", "owner", "creator"
            }
        except Exception:
            return False
    return False
