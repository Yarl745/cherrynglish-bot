import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, MediaGroup

import keyboards
from data.config import EXAMPLE_IMGS
from filters import IsUser
from loader import dp
from states.adding_set import AddingSet
from utils import clean_previous_menu_msg
from utils.db_api import redis_commands


@dp.message_handler(IsUser(), text="Добавить✨")
async def show_adding_info(msg: Message, state: FSMContext):
    user = types.User.get_current()

    help_album = get_help_album(
        caption="Для того чтобы добавить свой набор слов, нужно:\n"
                "1) cделать скриншоты слов, которы ты хочешь выучить;\n"
                "2) перейти в Cherrynglish бота;\n"
                "3) прикрепить все скриншоты слов, которые будут в твоём наборе.",
    )
    await msg.answer_media_group(
        media=help_album
    )
    await msg.answer(
        "Сначала прикрепи скриншоты:",
        reply_markup=keyboards.default.read_photo_menu
    )

    await clean_previous_menu_msg(msg, state)
    await state.finish()
    await redis_commands.clean_all_photo_ids(user.id)

    await AddingSet.read_photos.set()

    logging.info(f"Show adding set info for @{user.username}-{user.id}")


def get_help_album(caption: str):
    help_album = MediaGroup()
    for img_id in EXAMPLE_IMGS:
        help_album.attach_photo(
            img_id, caption=caption
        )
        caption = ""

    return help_album