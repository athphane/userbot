from pyrogram import Filters, Message
from time import sleep
from userbot import UserBot
from userbot.helpers.constants import Eval


@UserBot.on_message(Filters.command("eval", ".") & Filters.me)
async def evaluation(bot: UserBot, message: Message):
    try:
        cmdstr = " ".join(message.command[1:])
    except IndexError:
        await message.edit("__I can't evaluate nothing...__")
        sleep(2)
        await message.delete()
        return

    if cmdstr:
        expr = await message.reply(Eval.RUNNING.format(cmdstr))

        try:
            result = eval(cmdstr)
        except Exception as err:
            await expr.edit(Eval.ERROR.format(cmdstr, err))
        else:
            if result is None:
                await expr.edit(Eval.SUCCESS.format(cmdstr))
            elif len(Eval.RESULT.format(cmdstr, result)) > 4096:
                await expr.edit(Eval.RESULT_FILE.format(cmdstr))
                await bot.send_chat_action(message.chat.id, "upload_document")
            else:
                await expr.edit(Eval.RESULT.format(cmdstr, result))


@UserBot.on_message(Filters.command("exec", ".") & Filters.me)
async def execution(bot: UserBot, message: Message):
    try:
        cmdstr = message.text[6:]
    except IndexError:
        await message.edit("__I can't execute nothing...__")
        sleep(2)
        await message.delete()
        return

    if cmdstr:
        expr = await message.reply(Eval.RUNNING.format(cmdstr))
        try:
            exec(
                'def __ex(bot, message): '
                + ''.join(
                    '\n '
                    + l for l in cmdstr.split('\n')))
            result = locals()['__ex'](bot, message)
        except Exception as err:
            await expr.edit(Eval.ERROR.format(cmdstr, err))
        else:
            if result:
                await expr.edit(Eval.RESULT.format(cmdstr, result))
            else:
                await expr.edit(Eval.SUCCESS.format(cmdstr))
