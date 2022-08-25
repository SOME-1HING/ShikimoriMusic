import datetime
import platform
import time
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from ShikimoriMusic.mongo.chats import get_served_chats
from ShikimoriMusic.mongo.users import get_served_users
from ShikimoriMusic.setup.filters import command
from pyrogram import __version__ as pyrover
from pyrogram.types import Message
    
from ShikimoriMusic import starttime, pbot
from  ShikimoriMusic.vars import SUDO_USERS, SUPPORT_CHAT

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@pbot.on_message(command("stats"))
async def stats(_, message: Message):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - starttime))
    status = "*╒═══「 System statistics 」*\n\n"
    status += "*➢ System Start time:* " + str(uptime) + "\n"
    uname = platform.uname()
    status += "*➢ System:* " + str(uname.system) + "\n"
    status += "*➢ Node name:* " + (str(uname.node)) + "\n"
    status += "*➢ Release:* " + (str(uname.release)) + "\n"
    status += "*➢ Machine:* " + (str(uname.machine)) + "\n"
    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "*➢ CPU:* " + str(cpu) + " %\n"
    status += "*➢ RAM:* " + str(mem[2]) + " %\n"
    status += "*➢ Storage:* " + str(disk[3]) + " %\n\n"
    status += "*➢ Python Version:* " + python_version() + "\n"
    status += "*➢ Pyrogram Version:* " + str(pyrover) + "\n"
    status += "*➢ Uptime:* " + str(botuptime) + "\n"

    await message.reply_text(
        (
            (
                (
                    "*Bot statistics*:\n"
                    + f"**Served Chats:** {len(get_served_chats())}\n" 
                    + f"**Served Users:** {len(get_served_users())} "
                )
                + f"\n\n✦ [Support](https://t.me/{SUPPORT_CHAT})"
            )
        ),
        parse_mode="markdown",
    )