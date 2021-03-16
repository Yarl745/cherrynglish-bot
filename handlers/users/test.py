from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, ContentTypes
from asgiref.sync import sync_to_async
from PIL import Image

import keyboards
from loader import dp
from utils.photo_crop import get_drawn_img


@dp.message_handler(text="restart", state="*")
async def restart_state(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(
        f"Restart states!",
        reply_markup=keyboards.default.bot_menu
    )


@dp.message_handler(content_types=ContentTypes.PHOTO)
async def test_photo(msg: Message):
    photo = msg.photo[-1]
    file = BytesIO()
    await photo.download(destination=file)

    cropped_img_file: BytesIO = await get_drawn_img(file)
    await msg.answer_photo(InputFile(cropped_img_file))


@sync_to_async
def get_cropped_img_file(file):
    image: Image.Image = Image.open(file)

    # (x1, y1, x2, y2) upper left and lower right
    x1, y1, x2, y2 = image.getbbox()
    crop_img = image.crop((x1, y1, x2, y2//2))

    out_file = BytesIO()
    crop_img.save(out_file, format="png")

    out_file.seek(0)

    return out_file


