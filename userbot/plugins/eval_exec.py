import asyncio
import io
import os
import sys
import traceback
import re
from typing import Optional

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.database import database
from userbot.helpers.PyroHelpers import ReplyCheck


@UserBot.on_message(
    filters.command("eval", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def eval_func_init(bot, message):
    await evaluation_func(bot, message)


@UserBot.on_edited_message(
    filters.command("eval", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def eval_func_edited(bot, message):
    await evaluation_func(bot, message)


@UserBot.on_message(
    filters.command("math", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def math_func_init(bot, message):
    await math_evaluation(bot, message)


@UserBot.on_edited_message(
    filters.command("math", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def math_func_edited(bot, message):
    await math_evaluation(bot, message)


async def evaluation_func(
    bot: UserBot,
    message: Message,
    cmd_override: Optional[str] = None,
    display_override: Optional[str] = None,
):
    status_message = await message.reply_text("Processing ...")
    if cmd_override is not None:
        cmd = cmd_override
    else:
        if len(message.text.split(" ", maxsplit=1)) < 2:
            await status_message.edit("No expression provided.")
            return
        cmd = message.text.split(" ", maxsplit=1)[1]

    display_cmd = display_override if display_override is not None else cmd

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        reply = message.reply_to_message or None
        await aexec(cmd, bot, message, reply, database)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>Expression</b>:\n<code>{}</code>\n\n<b>Result</b>:\n<code>{}</code> \n".format(
        display_cmd, evaluation.strip()
    )

    if len(final_output) > 4096:
        with open("eval.txt", "w", encoding="utf8") as out_file:
            out_file.write(str(final_output))

        await message.reply_document(
            "eval.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=ReplyCheck(message),
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, b, m, r, d):
    sys.tracebacklimit = 0
    exec(
        "async def __aexec(b, m, r, d): "
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](b, m, r, d)


async def math_evaluation(bot: UserBot, message: Message):
    parts = message.text.split(" ", maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.reply_text("Please provide a mathematical expression to evaluate.")
        return

    expression = re.sub(r"\+(\d+)%", lambda m: str(1+(int(m.group(1))/100)), parts[1])
    cmd = f"print({expression})"
    await evaluation_func(bot, message, cmd_override=cmd, display_override=expression)


@UserBot.on_edited_message(
    filters.command("exec", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def execution_func_edited(bot, message):
    await execution(bot, message)


@UserBot.on_message(
    filters.command("exec", ".")
    & filters.me
    & ~filters.forwarded
    & ~filters.via_bot
)
async def execution_func(bot, message):
    await execution(bot, message)


async def execution(bot: UserBot, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No errors"
    o = stdout.decode()
    if not o:
        o = "No output"

    OUTPUT = ""
    OUTPUT += f"<b>Command:</b>\n<code>{cmd}</code>\n\n"
    OUTPUT += f"<b>Output</b>: \n<code>{o}</code>\n"
    OUTPUT += f"<b>Errors</b>: \n<code>{e}</code>"

    if len(OUTPUT) > 4096:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=ReplyCheck(message),
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)
