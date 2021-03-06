import logging
from io import BytesIO

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes, Message, ReplyKeyboardRemove, MediaGroup, InputMediaPhoto, User

import keyboards
from handlers.users.add_set.click_add import show_adding_info
from loader import dp, db, bot
from states.adding_set import AddingSet
from utils.db_api import redis_commands
from utils.misc import rate_limit
from utils.photo_crop import get_drawn_img, get_separated_imgs


@rate_limit(0)
@dp.message_handler(state=AddingSet.read_set_name, content_types=ContentTypes.PHOTO)
@dp.message_handler(state=AddingSet.read_photos, content_types=ContentTypes.PHOTO)
async def read_photo(msg: Message):
    user = msg.from_user
    await msg.bot.send_chat_action(msg.chat.id, 'upload_photo')
    photo_id = msg.photo[-1].file_id
    await redis_commands.push_photo_id(user.id, photo_id)


@dp.message_handler(state=AddingSet.read_photos, text="Продолжить⏩")
async def save_photos(msg: Message):
    user = msg.from_user
    photo_ids = await redis_commands.get_all_photo_ids(user.id)

    if not photo_ids:
        await msg.answer("Сначала прикрепи скриншоты для своего набора 🥴")
        return

    await msg.answer(
        "Придумай название для своего набора слов:",
        reply_markup=ReplyKeyboardRemove()
    )

    await AddingSet.read_set_name.set()

    logging.info(f"For @{user.username}-{user.id} save photos in redis len({len(photo_ids)})")


@dp.message_handler(state=AddingSet.read_photos, text="Отменить↩️")
async def cancel_creating_set(msg: Message, state: FSMContext):
    user = msg.from_user

    await msg.answer(
        "Создание набора отменено.",
        reply_markup=keyboards.default.get_bot_menu()
    )
    await msg.answer_sticker("CAACAgIAAxkBAAPMYE3_4aKH6ddyThPFL2npELzRzVUAAhAAA8A2TxPqgYop8R8C6B4E")

    await state.finish()

    logging.info(f"@{user.username}-{user.id} cancel creating set")


@dp.message_handler(state=AddingSet.read_set_name)
async def read_set_name(msg: Message, state: FSMContext):
    user = msg.from_user
    set_name = msg.text

    if len(set_name) > 50:
        await msg.answer(
            "Название набора не должно первышать 50 символов 🥴\n"
            "Попробуй ввести его ещё раз:"
        )
        return
    await state.update_data(set_name=set_name)

    photo_id: str = await redis_commands.get_photo_id(user.id)
    await msg.bot.send_chat_action(user.id, "upload_photo")

    img_file = BytesIO()
    await (await msg.bot.get_file(photo_id)).download(destination=img_file)
    drawn_img = await get_drawn_img(img_file)

    crop_range_str = await redis_commands.get_last_crop_range_str(user.id)
    await msg.answer_photo(
        drawn_img,
        caption="Введи диапозон высот по которому обрежется часть "
                "картинки с английским словом и с переводом.\n\n"
                "Диапозон: верхняя граница слова, граница между словом и переводом, "
                "нижняя граница слова.\n\n"
                "<i>Пример ввода: 300 470 1150</i>",
        reply_markup=keyboards.default.get_text_menu(crop_range_str) if crop_range_str else ReplyKeyboardRemove()
    )

    await AddingSet.config_sizes.set()

    logging.info(f"@{user.username}-{user.id} read set name {set_name}")


@dp.message_handler(state=AddingSet.config_sizes, text="🔸Создать набор🔸")
async def save_set(msg: Message, state: FSMContext):
    user = msg.from_user

    await msg.bot.send_chat_action(user.id, "upload_photo")
    await AddingSet.loading_data.set()
    await msg.answer("Загрузка набора...")
    await msg.answer_sticker(
        "CAACAgIAAxkBAAEIxr1gV8whFcjH7n98RLQQKls9mGg49QACGAADwDZPE9b6J7-cahj4HgQ",
        reply_markup=ReplyKeyboardRemove()
    )

    data = await state.get_data()
    crop_range = data["crop_range"]
    set_name = data["set_name"]
    photo_ids = await redis_commands.get_all_photo_ids(user.id)
    await redis_commands.clean_all_photo_ids(user.id)

    set_id = await db.add_set(
        user_id=user.id,
        name=set_name
    )

    words_data = await prepare_words_data(set_id, photo_ids, crop_range)

    if not words_data:
        await msg.answer("Ты задал(-а) дипазон, который выходит за пределы размера какого-то "
                         "твоего скриншота 🥴\n"
                         "Постарайся добавлять скриншоты одного размера!")
        await db.delete_set(set_id)
        await show_adding_info(msg, state)
        return

    logging.info(f"Prepared words_data[len-{len(words_data)}] for @{user.username}-{user.id}")

    for word_data in words_data:
        await db.add_word(**word_data)

    await redis_commands.set_last_crop_range(user.id, crop_range)

    await msg.answer(
        "Твой набор слов был успеешно создан!",
        reply_markup=keyboards.default.get_bot_menu()
    )
    await msg.answer_sticker("CAACAgIAAxkBAAIB-2BQzR9z-1xm1HM6zK9C_yBuTwgdAAIdAAPANk8TXtim3EE93kgeBA")

    await state.finish()
    logging.info(f"Created new set {set_name}-{set_id} for @{user.username}-{user.id}")


@dp.message_handler(state=AddingSet.config_sizes)
async def config_crop_range(msg: Message, state: FSMContext):
    user = msg.from_user
    crop_range_str = msg.text

    if not crop_range_str.replace(" ", "").isdecimal() or len(crop_range_str.split(" ")) != 3:
        await msg.answer(
            "Вводить диапазон нужно тремя целыми числами, через пробел 🥴\n"
            "<i>Пример ввода: 300 470 1150</i>"
        )
        return
    elif len(crop_range_str) > 25:
        await msg.answer(
            "Какие-то очень большие размеры для обрезания картинки 🥴\n"
            "На самой первой тестовой картинке отмечены границы высоты зелённой линией."
        )

    crop_range = [int(num) for num in crop_range_str.split(" ")]
    crop_range.sort()

    photo_id: str = await redis_commands.get_photo_id(user.id)
    await msg.bot.send_chat_action(user.id, "upload_photo")

    img_file = BytesIO()
    photo = await msg.bot.get_file(photo_id)
    await photo.download(destination=img_file)

    word_img, transl_img = await get_separated_imgs(img_file, *crop_range)

    if not word_img:
        await msg.answer("Ты задал(-а) дипазон, который выходит за пределы размера картинки 🥴\n"
                         "На картинке с зелённой линией показаны допустимые для тебя значения высоты.")
        return

    separated_imgs_album = MediaGroup()
    separated_imgs_album.attach_many(
        InputMediaPhoto(word_img),
        InputMediaPhoto(transl_img)
    )

    await state.update_data(crop_range=crop_range)

    await msg.answer_media_group(separated_imgs_album)
    await msg.answer(
        "Если фотографии обрезалась не корректно, то введи "
        "диапозон высот ещё раз.",
        reply_markup=keyboards.default.create_set_menu
    )

    logging.info(f"@{user.username}-{user.id} read crop_range {crop_range}")


async def prepare_words_data(set_id: int, photo_ids: list, crop_range: list) -> list:
    words_data = []
    user_id = User.get_current().id

    for photo_id in photo_ids:
        img_file = BytesIO()
        await (await bot.get_file(photo_id)).download(destination=img_file)
        word_img, transl_img = await get_separated_imgs(img_file, *crop_range)
        logging.info(f" --- {word_img} --- {transl_img} ---")

        # If some img from the range smaller than the crop size
        if not word_img:
            return None

        word_img_msg = await bot.send_photo(user_id, word_img)
        word_img_id = word_img_msg.photo[-1].file_id
        await word_img_msg.delete()

        transl_img_msg = await bot.send_photo(user_id, transl_img)
        transl_img_id = transl_img_msg.photo[-1].file_id
        await transl_img_msg.delete()

        words_data.append(dict(
            set_id=set_id,
            base_img_id=photo_id,
            word_img_id=word_img_id,
            transl_img_id=transl_img_id
        ))

    return words_data
