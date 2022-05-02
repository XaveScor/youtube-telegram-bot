import logging
import os.path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import input_file
from yt_dlp import YoutubeDL
import tempfile

API_TOKEN = os.getenv('TG_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)