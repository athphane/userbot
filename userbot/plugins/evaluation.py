from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import Eval
from time import sleep


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
            else:
                await expr.edit(Eval.RESULT.format(cmdstr, result))
