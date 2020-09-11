from aiohttp.client_exceptions import ClientError
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot, ALLOWED_USERS
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help

text_apis_data = {
    'compliment': {'url': 'https://complimentr.com/api', 'target_key': 'compliment',
                   'help': 'Sends a nice compliment.'},
    'devexcuse': {'url': 'https://dev-excuses-api.herokuapp.com/', 'target_key': 'text',
                  'help': 'It works on my machine!'},
    'insult': {'url': 'https://evilinsult.com/generate_insult.php?lang=en', 'target_key': 'insult',
               'help': 'Give it a guess dumbass!'},
    'kanye': {'url': 'https://api.kanye.rest/', 'target_key': 'quote', 'format': 'Kanye once said:\n`{}`',
              'help': 'Kanye used to say'},
    'programmer': {'url': 'https://programming-quotes-api.herokuapp.com/quotes/random', 'target_key': 'en',
                   'help': 'Programmers be like.'},
    'affirmation': {'url': 'https://www.affirmations.dev/', 'target_key': 'affirmation',
                    'help': 'Affirmative messages'}
}

text_api_commands = []
for x in text_apis_data:
    text_api_commands.append(x)
    if 'alts' in text_apis_data[x]:
        for y in text_apis_data[x]['alts']:
            text_api_commands.append(y)


@UserBot.on_message(filters.command(text_api_commands, '.') & (filters.me | filters.user(ALLOWED_USERS)))
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
            if message.from_user.is_self:
                await message.edit(txt)
            else:
                await message.reply(txt)
        except Exception:
            data = await AioHttp().get_text(api['url'])
            if message.from_user.is_self:
                await message.edit(data)
            else:
                await message.reply(data)
    except ClientError as e:
        print(e)
        await message.delete()


# Command help section
for x in text_apis_data:
    add_command_help(
        'text', [
            [f'.{x}', text_apis_data[x]['help']],
        ]
    )
