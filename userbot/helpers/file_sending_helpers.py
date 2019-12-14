import json
from pyrogram import Message
from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck, GetChatID


def get_old_message(message_id, media_type):
    old_message = BOT.get_messages('self', message_id)

    if media_type is "photo":
        return old_message.photo

    if media_type is "animation":
        return old_message.animation


# Save the sent media's ID to file to send faster next time
def save_media_id(name, media: Message):
    file_json = json.load(open("file_ids.txt", "r"))
    message_id = media.message_id
    file_json[name] = message_id
    f = open("file_ids.txt", "w")
    f.write(json.dumps(file_json))
    f.close()


# Function to reuse to send animation and remember the file_id
async def send_saved_animation(message: Message, name: str, image: str):
    id_list = json.load(open("file_ids.txt", "r"))

    if name in id_list:
        old_message = get_old_message(int(id_list[name]), "animation")
        await UserBot().send_animation(
            GetChatID(message),
            old_message.file_id,
            file_ref=old_message.file_ref,
            reply_to_message_id=ReplyCheck(message)
        )
    else:
        sent_animation = await UserBot().send_animation(
            "self",
            "userbot/images/{}".format(image),
            reply_to_message_id=ReplyCheck(message)
        )
        save_media_id(name, sent_animation)
        await send_saved_animation(message, name, image)


# Function to reuse to send image and save file_id
async def send_saved_image(message: Message, name: str, image: str):
    thing = json.load(open("file_ids.txt", "r"))

    if name in thing:
        old_message = get_old_message(int(thing[name]), "photo")
        await UserBot().send_photo(
            GetChatID(message),
            old_message.file_id,
            file_ref=old_message.file_ref,
            reply_to_message_id=ReplyCheck(message)
        )
    else:
        sent_photo = await UserBot().send_photo(
            "self",
            "images/{}".format(image),
            reply_to_message_id=ReplyCheck(message)
        )
        save_media_id(name, sent_photo)
        await send_saved_image(message, name, image)
