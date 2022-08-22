from asyncio import QueueEmpty
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from ShikimoriMusic.mongo.queue import remove_active_chat
from ShikimoriMusic.calls import queues
from ShikimoriMusic import pytgcalls

@pytgcalls.on_kicked()
async def on_kicked(client: PyTgCalls, chat_id: int) -> None:
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)


@pytgcalls.on_closed_voice_chat()
async def on_closed(client: PyTgCalls, chat_id: int) -> None:
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)


@pytgcalls.on_stream_end()
async def on_stream_end(client: PyTgCalls, update: Update) -> None:
    chat_id = update.chat_id
    try:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await pytgcalls.leave_group_call(chat_id)
        else:
            await pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        queues.get(chat_id)["file"],
                    ),
                ),
            )

    except Exception as e:
        print(e)

run = pytgcalls.start
