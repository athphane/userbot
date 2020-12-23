import asyncio

from pyrogram import filters
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("setpic", ".") & filters.me)
async def set_picture(_, message: Message):
    # First of all check if its a group or not
    if message.chat.type in ["group", "supergroup"]:
        # Here lies the sanity checks
        admins = await UserBot.get_chat_members(
            message.chat.id, filter=ChatMemberFilters.ADMINISTRATORS
        )
        admin_ids = [user.user.id for user in admins]
        me = await UserBot.get_me()

        # If you are an admin
        if me.id in admin_ids:

            my_permissions = None
            # Fetch your permissions
            for user in admins:
                if user.user.id == me.id:
                    my_permissions = user

            # If you can change group photo
            if my_permissions and my_permissions.can_change_info:
                # If you replied to a message and it has a photo
                if message.reply_to_message and message.reply_to_message.media:
                    file_id = message.reply_to_message.photo.file_id
                    file_ref = message.reply_to_message.photo.file_ref
                    await UserBot.set_chat_photo(
                        message.chat.id, file_id, file_ref=file_ref
                    )
                    await message.edit(
                        f"`{message.chat.type.title()} picture has been set.`"
                    )
                    return
                else:
                    # You didn't reply and it didn't have a photo either. Baka.
                    await message.edit(
                        f"`Please reply to a message with a photo to set it as {message.chat.type} picture.`"
                    )
            else:
                # You literally CANNOT do this.
                await message.edit("`I lack the permissions to do this...`")
        else:
            # You have no business running this command.
            await message.edit("`I am not an admin here.`")
    else:
        # Are you fucking dumb this is not a group ffs.
        await message.edit("`This is not a place where I can change the picture.`")

    # And of course delete your lame attempt at changing the group picture.
    # RIP you.
    # You're probably gonna get ridiculed by everyone in the group for your failed attempt.
    # RIP.
    await asyncio.sleep(3)
    await message.delete()


# Command help section
add_command_help("admin", [[".setpic", "Set group picture as the replied to photo."]])
