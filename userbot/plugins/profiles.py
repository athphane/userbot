import asyncio

from pyrogram import filters
from pyrogram.errors import UsernameOccupied
from pyrogram.types import Message

from userbot import UserBot
from userbot.database.profiles import Profiles
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("profiles", ".") & filters.me)
async def profile_list(_, message: Message):
    profiles = Profiles().all_profiles()
    for x in profiles:
        print(x)

    await message.edit('All available profiles.')


@UserBot.on_message(filters.command("profilecreate", ".") & filters.me)
async def profile_create(bot: UserBot, message: Message):
    if not len(message.command) > 2:
        await message.edit('Insufficient number of arguments.\nRequired: Name and Username')
        await asyncio.sleep(3)
        await message.delete()
        return

    title = message.command[1]
    username = message.command[2]
    created_channel = await bot.create_channel(title, f"Username backup channel for {username}")

    print(created_channel)

    try:
        await bot.update_chat_username(created_channel.id, username)
    except UsernameOccupied:
        await bot.delete_channel(created_channel.id)
        await message.edit("The username is not available! **Aborting**.")
        return

    Profiles().add_profile(created_channel.id, created_channel.title, username)
    await message.edit(f"Profile Created.\nName: {username}")


@UserBot.on_message(filters.command("profile", ".") & filters.me)
async def switch_profiles(bot: UserBot, message: Message):
    if not len(message.command) > 1:
        await message.edit('Profile not specified.')
        return

    try:
        profile_number = int(message.command[1])
    except ValueError:
        await message.edit("Please enter a number.")
        await asyncio.sleep(3)
        await message.delete()
        return

    profile_to = Profiles().getProfile(profile_number)

    if profile_to is not None:
        profile_to_channel = await bot.get_chat(profile_to['channel_id'])
        await bot.update_chat_username(profile_to['channel_id'], profile_to['username'] + '_inUse')

        # Remove username from target profile channel
        # Remove username from current profile

        # Check if there is a backup channel for real profile
        # Create real username channel and save.
        #
        print("hits'")
        # Ready to start profile switching.
        pass


# Command help section
add_command_help(
    "profiles",
    [
        [".profiles", "List all available profiles."],
        [".profile", "Profile changed to the selected profile"],
    ],
)
