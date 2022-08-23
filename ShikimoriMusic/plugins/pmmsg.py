# Copyright (©️) @KIRITO_1240
# By : KIRITO

from pyrogram import Client
from ShikimoriMusic.calls import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User
from ShikimoriMusic.config import (
    BOT_USERNAME,
)

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"Hey 👋 I am the assistant of Shikimori Music bot, didn't have a time to talk with you 🙂 kindly join @LigmaSupport for getting Support.")
  return
