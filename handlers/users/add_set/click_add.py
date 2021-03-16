import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, MediaGroup

import keyboards
from data.config import EXAMPLE_IMGS
from filters import IsUser
from loader import dp
from states.adding_set import AddingSet


@dp.message_handler(IsUser(), text="Добавить✨")
async def show_adding_info(msg: Message, state: FSMContext):
    user = msg.from_user

    help_album = get_help_album(
        caption="Для того чтобы добавить свой набор слов, нужно:\n"
                "1) cделать скриншоты слов, которы ты хочешь выучить;\n"
                "2) перейти в Cherrynglish бота;\n"
                "3) прикрепить все скриншоты слов, которые будут в твоём наборе."
    )
    await msg.answer_media_group(
        media=help_album,
    )
    await msg.answer(
        "После этих шагов автоматически начнётся процесс создания твоего набора 😉",
        reply_markup=keyboards.default.read_photo_menu
    )

    await AddingSet.read_photos.set()
    await state.update_data(photo_ids=[])

    logging.info(f"Show adding set info for @{user.username}-{user.id}")


def get_help_album(caption: str):
    help_album = MediaGroup()
    for img_id in EXAMPLE_IMGS:
        help_album.attach_photo(
            img_id, caption=caption
        )
        caption = ""

    return help_album