import logging
import os.path

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import input_file
from yt_dlp import YoutubeDL
import tempfile

API_TOKEN = os.getenv('TG_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

logging.basicConfig(level=logging.INFO)

event_loop = asyncio.new_event_loop()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, loop=event_loop)


@dp.message_handler()
async def download_video(message: types.Message):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with YoutubeDL({
            'outtmpl': {
                'default': os.path.join(tmpdirname, '%(title)s.%(ext)s'),
            }
        }) as ydl:
            info = ydl.extract_info(message.text, download=True)
            file = input_file.InputFile(path_or_bytesio=ydl.prepare_filename(info))
            await message.answer_video(video=file)


async def on_startup():
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text="bot redeployed")


if __name__ == '__main__':
    event_loop.run_until_complete(on_startup())
    executor.start_polling(dp, skip_updates=False)
