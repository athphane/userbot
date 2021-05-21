from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

maid_sticker_ids = {
    'CAACAgIAAxkBAAI2iWCnpwvltl2NicJ1_Qp71guEQKRhAALYeAACY4tGDKVjsbi0L8axHgQ': [
        'CAACAgIAAxkBAAI2eWCnpC1x6tam75lda5gkuXI0z0VNAALdeAACY4tGDNmsCquwdRiKHgQ',
        'CAACAgIAAxkBAAI2e2CnpC4GuhZXbp2iH8QIRSZJ_mtOAALieAACY4tGDARcnUmP7bYsHgQ'],
    'CAACAgIAAxkBAAI2fWCnpGQSDZ8rWWgil0SaI90U8ZNjAAL0eAACY4tGDIqUzLJoaTt5HgQ': [
        'CAACAgIAAxkBAAI2f2CnpGYXNJeotktonLteN7yN350yAAL5eAACY4tGDH8Bec87XLfbHgQ',
        'CAACAgIAAxkBAAI2gWCnpGaWuJV0xy6xIfvfSG_neNBCAAL-eAACY4tGDLgORLtAeMmiHgQ']
}


@UserBot.on_message(filters.user(352665135) & filters.sticker)
async def maid_stickers(bot: UserBot, message: Message):
    sticker_id = message.sticker
    print(sticker_id)

    # if sticker_id in maid_sticker_ids.keys():
    #     print(sticker_id)
    #     await bot.send_sticker(message.chat.id, sticker_id)
        # for sticker in maid_sticker_ids[sticker_id]:
        #     await bot.send_sticker(message.chat.id, sticker, disable_notification=True)



# Command help section
add_command_help(
    "maid-stickers",
    [
        [".none", "Nothing yet."],
    ],
)
