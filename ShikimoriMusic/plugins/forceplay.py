import asyncio
import os
import requests

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant

from ShikimoriMusic.calls import calls, queues
from ShikimoriMusic.calls.youtube import download
from ShikimoriMusic.plugins.play import generate_cover
from ShikimoriMusic.calls import convert as cconvert
from ShikimoriMusic.mongo.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
)
from ShikimoriMusic import pbot, ubot
from ShikimoriMusic.vars import (
    DURATION_LIMIT,
    que,
    SUPPORT_CHAT,
    UPDATE,
)
from ShikimoriMusic import ASS_USERNAME, BOT_ID, ASS_NAME, ASS_ID, BOT_NAME, BOT_USERNAME
from ShikimoriMusic.setup.filters import command
from ShikimoriMusic.setup.errors import DurationLimitError
from ShikimoriMusic.setup.gets import get_url, get_file_name

# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
flex = {}


# play
@Client.on_message(
    command(["playforce", f"playforce@{BOT_USERNAME}"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    user_id = message.from_user.id
    if message.sender_chat:
        return await message.reply_text(
            " __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )

    if message.chat.id in DISABLED_GROUPS:
        await message.reply(
            " __**Music player is turned off, ask the admin to turn on it on!**__"
        )
      

        return
    lel = await message.reply("**ᴘʀᴏᴄᴇssɪɴɢ.....**")

    chid = message.chat.id

    c = await pbot.get_chat_member(message.chat.id, BOT_ID)
    if c.status != "administrator":
        await lel.edit(
            f"**ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀ ᴀᴅᴍɪɴ !!**"
        )
        return
    if not c.can_manage_voice_chats:
        await lel.edit(
            "**ᴍᴀɴᴀɢᴇ-ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ : ᴘᴏᴡᴇʀ ❌**"
        )
        return
    if not c.can_delete_messages:
        await lel.edit(
            "**ᴅᴇʟᴇᴛᴇ-ᴍᴇssᴀɢᴇ : ᴘᴏᴡᴇʀ ❌**"
        )
        return
    if not c.can_invite_users:
        await lel.edit(
            "**ɪɴᴠɪᴛᴇ-ᴜsᴇʀs : ᴘᴏᴡᴇʀ ❌**"
        )
        return

    try:
        b = await pbot.get_chat_member(message.chat.id, ASS_ID)
        if b.status == "kicked":
            await message.reply_text(
                f"🔴 {ASS_NAME} (@{ASS_USERNAME}) is banned in your chat **{message.chat.title}**\n\nUnban it first to use music"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ubot.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"**@{ASS_USERNAME} joined !**",
                )
                remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f"**@{ASS_USERNAME} failed to join** Add @{ASS_USERNAME} manually in your group.\n\n**Reason**:{e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                    link_bokep = f"https://t.me/joinchat/{kontol}"
                await ubot.join_chat(link_bokep)
                await message.reply(
                    f"**@{ASS_USERNAME} joined successfully**",
                )
                remove_active_chat(message.chat.id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"**@{ASS_USERNAME} failed to join** Add @{ASS_USERNAME} manually in your group.\n\n**Reason**:{e}"
                )

    await message.delete()
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        url = f"https://t.me/{UPDATE}"
        title = audio.title
        thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url="https://youtube.com"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await cconvert(
            (await message.reply_to_message.download(file_name))
            if not os.path.isfile(os.path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url="https://youtube.com"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ {title[:50]}\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}..\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** {title[:50]}...\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}....\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴘʀᴏɢʀᴇss :** {percentage}\n**sᴘᴇᴇᴅ :** {speed}\n**ᴇᴛᴀ :** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ :** {title[:50]}.....\n\n**ғɪʟᴇ sɪᴢᴇ :** {size}\n**ᴛɪᴍᴇ :** {taken} sec\n\n**ᴄᴏɴᴠᴇʀᴛɪɴɢ ғɪʟᴇ : **[__FFmpeg processing__]"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "❌ ᴀʟsᴏ ɢɪᴠᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ ᴡɪᴛʜ ᴜsɪɴɢ ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅ !!\n\nғᴏʀ ᴇxᴀᴍᴘʟᴇ :\n/play 295"
            )
        await lel.edit("**ғɪɴᴅɪɴɢ 🔎 sᴇʀᴠᴇʀ !!**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**ɢᴇᴛᴛɪɴɢ..... ʀᴇsᴘᴏɴsᴇ.....**")
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "• **Song not found**\n\nwrite name correctly."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("🎥 ᴡᴀᴛᴄʜ", url="https://youtube.com"),
            InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ],[
            InlineKeyboardButton("🚫 ᴄʟᴏsᴇ", callback_data="cls"),
        ],
        
    ]
)

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"**ᴄᴏɴɴᴇᴄᴛɪɴɢ 🔄**"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴘʀᴏᴄᴇssɪɴɢ.....**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴄᴏɴɴᴇᴄᴛɪɴɢ 🔄**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**ᴘʀᴏᴄᴇssɪɴɢ.....**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**ᴅᴏᴡɴʟᴏᴀᴅ ғɪɴɪsʜ !!**\n\n**{title[:50]}...\n\n**ғɪʟᴇ sɪᴢᴇ : {size}**\n■■■■■■■■■■ `100%`\n**ᴛɪᴍᴇ : {taken} sec**\n\n<b> ғғᴍᴘᴇᴊ ʀᴜɴɴɪɴɢ....</b>"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert.convert(x)

    if is_active_chat(message.chat.id):
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**[ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴠɪᴀ ʏᴏᴜᴛᴜʙᴇ 📡]({})**\n\n• ᴜsᴇʀ : {}\n• ɢʀᴏᴜᴘ : [{}](https://t.me/{})".format(
                url, message.from_user.mention(), message.chat.title, message.chat.username
            ),
        )
    else:
        try:
            await calls.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception:
            return await lel.edit(
                "Error Joining Voice Chat. Make sure Voice Chat is Enabled.\n\n If YES, then make sure Music Bots Assistant is not banned in your group or available in your group!"
            )


        music_on(message.chat.id)
        add_active_chat(message.chat.id)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**[ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴠɪᴀ ʏᴏᴜᴛᴜʙᴇ 📡]({})**\n\n• ᴜsᴇʀ : {}\n• ɢʀᴏᴜᴘ : [{}](https://t.me/{})".format(
                url, message.from_user.mention(), message.chat.title, message.chat.username
            ),
        )

    os.remove("final.png")
    return await lel.delete()
