import logging
import os.path
import re
import asyncio
import tempfile

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import input_file
from yt_dlp import YoutubeDL
import ffmpeg

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
            },
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }) as ydl:
            info = ydl.extract_info(message.text, download=True)
            # Пока так. Как доставать реальный формат файла я не нашёл
            filename = re.sub(r'\.webm$', '.m4a', ydl.prepare_filename(info))

            duration = ffmpeg.probe(filename)['format']['duration']
            file = input_file.InputFile(path_or_bytesio=filename)
            await message.answer_audio(
                audio=file,
                duration=duration
            )


async def on_startup():
    if ADMIN_CHAT_ID is not None:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text="bot redeployed")


if __name__ == '__main__':
    event_loop.run_until_complete(on_startup())
    executor.start_polling(dp, skip_updates=False)
