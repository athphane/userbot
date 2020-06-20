import asyncio

from pyrogram import Filters, Message

from userbot import UserBot, CMD_HELP


@UserBot.on_message(Filters.command("help", ".") & Filters.me)
async def module_help(_, message: Message):
    cmd = message.command

    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        all_commands = ""

        all_commands += "Please specify which module you want help for!! \nUsage: `.help [module_name]`\n\n"

        for x in CMD_HELP:
            all_commands += f"`{x}`\n"

        await message.edit(all_commands)

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = ""
            this_command += f"--**Help for {str(help_arg)} module**--\n".upper()

            for x in commands:
                this_command += f"**{str(x)}**:\n```{str(commands[x])}```\n\n"

            await message.edit(this_command, parse_mode='markdown')
        else:
            await message.edit('`Please specify a valid module name.`', parse_mode='markdown')

    await asyncio.sleep(10)
    await message.delete()


def add_command_help(module_name, commands):
    """
    Adds a modules help information.
    :param module_name: name of the module
    :param commands: list of lists, with command and description each.
    """

    # Key will be group name
    # values will be dict of dicts of key command and value description

    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict
