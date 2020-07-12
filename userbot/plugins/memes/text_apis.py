from aiohttp.client_exceptions import ClientError
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help

text_apis_data = {
    'compliment': {'url': 'https://complimentr.com/api', 'target_key': 'compliment'},
    'devexcuse': {'url': 'https://dev-excuses-api.herokuapp.com/', 'target_key': 'text'},
    'insult': {'url': 'https://evilinsult.com/generate_insult.php?lang=en', 'target_key': 'insult'},
    'kanye': {'url': 'https://api.kanye.rest/', 'target_key': 'quote', 'format': 'Kanye once said:\n`{}`'},
}

text_apis = [x for x in text_apis_data]


@UserBot.on_message(Filters.command(text_apis, '.') & Filters.me)
async def text_api(_, message: Message):
    cmd = message.command
    api_key = cmd[0]
    api = text_apis_data[api_key]

    try:
        try:
            data = await AioHttp().get_json(api['url'])
            resp_json = data[api['target_key']]
            if 'format' in api:
                txt = api['format'].format(resp_json)
            else:
                txt = resp_json.capitalize()
            await message.edit(
                txt
            )
        except Exception:
            data = await AioHttp().get_text(api['url'])
            await message.edit(data)
    except ClientError as e:
        print(e)
        await message.delete()


# Command help section
add_command_help(
    'text', [
        ['.compliment', 'Replaces command with a nice compliment.'],
        ['.devexcuse', 'Replaces command with an excuse that a developer would give.'],
        ['.insult', 'It does what it says it does.'],
        ['.kanye', 'Kanye once said...'],
    ]
)
