import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

import keyboards
from utils.change_bot_menu import change_bot_menu
from utils.repeat_notifications.notify_to_repeat import schedule_repeat
from keyboards.inline.sets_menu import sets_menu_callback
from keyboards.inline.word_menu import word_menu_callback
from loader import dp, db, bot
from utils import clean_previous_menu_msg


@dp.callback_query_handler(sets_menu_callback.filter(action="open_set"))
async def open_set(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user
    set_id = int(callback_data["set_id"])
    set_name = callback_data["set_name"]

    word_ids = [word["word_id"] for word in await db.get_shuffled_word_ids(set_id)]
    word = dict(await db.get_word_side(word_ids.pop(0)))

    learn_words_msg_id = (await msg.answer_photo(
        word.pop("word_img_id"),
        reply_markup=keyboards.inline.get_word_menu(word=word)
    )).message_id

    await clean_previous_menu_msg(msg, state)
    await state.finish()

    await state.update_data(
        word_ids=word_ids,
        set_id=set_id,
        set_name=set_name,
        learn_words_msg_id=learn_words_msg_id
    )

    await change_bot_menu(state)

    await call.answer()

    logging.info(f"@{user.username}-{user.id} starts learn set: {set_name}")


@dp.callback_query_handler(word_menu_callback.filter(action="know_word"))
async def know_word(call: CallbackQuery, state: FSMContext):
    msg = call.message
    user = call.from_user

    try:
        async with state.proxy() as data:
            word_id = int(data["word_ids"].pop(0))
        word = dict(await db.get_word_side(word_id))

        await msg.edit_media(
            InputMediaPhoto(word.pop("word_img_id")),
            reply_markup=keyboards.inline.get_word_menu(word=word)
        )
    except IndexError:
        await msg.delete()
        await msg.answer("Поздравляю! Теперь ты знаешь этот набор.",
                         reply_markup=keyboards.default.get_bot_menu())
        await msg.answer_sticker("CAACAgIAAxkBAAEIu69gVLjRs19x-GQrM1RvAjXPc9HFXAACHQADwDZPE17YptxBPd5IHgQ")

        data = await state.get_data()
        await schedule_repeat(user.id, data["set_id"], data["set_name"])

        await state.finish()
        return

    await call.answer()

    logging.info(f"@{user.username}-{user.id} know word -- {word_id}")


@dp.callback_query_handler(word_menu_callback.filter(action="dont_know_word"))
async def dont_know_word(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user
    unknown_word_id = int(callback_data["word_id"])

    async with state.proxy() as data:
        data["word_ids"].append(unknown_word_id)
        word_id = data["word_ids"].pop(0)
    word = dict(await db.get_word_side(word_id))

    await msg.edit_media(
        InputMediaPhoto(word.pop("word_img_id")),
        reply_markup=keyboards.inline.get_word_menu(word=word)
    )

    await call.answer()

    logging.info(f"@{user.username}-{user.id} dont know word -- {word_id}")


@dp.callback_query_handler(word_menu_callback.filter(action="change_side"))
async def change_side(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user
    side = callback_data["side"]
    word_id = int(callback_data["word_id"])

    if side == "word":
        word = dict(await db.get_transl_side(word_id))
        await msg.edit_media(
            InputMediaPhoto(word.pop("transl_img_id"), caption=word.pop("assoc")),
            reply_markup=keyboards.inline.get_word_menu(word=word, side=side)
        )
    elif side == "transl":
        word = dict(await db.get_word_side(word_id))
        await msg.edit_media(
            InputMediaPhoto(word.pop("word_img_id")),
            reply_markup=keyboards.inline.get_word_menu(word=word, side=side)
        )

    await call.answer()

    logging.info(f"@{user.username}-{user.id} change side of the word -- {word_id}")


@dp.callback_query_handler(word_menu_callback.filter(action="add_assoc"))
async def ask_add_assoc(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user
    word_id_for_assoc = int(callback_data["word_id"])

    ask_msg = await msg.answer(
        "Введи свою ассоциацию для этого слова:",
        reply_markup=keyboards.default.read_assoc_menu
    )

    await state.set_state("read_assoc")

    await state.update_data(
        word_id_for_assoc=word_id_for_assoc,
        ask_msg_id=ask_msg.message_id,
    )

    await call.answer()

    logging.info(f"@{user.username}-{user.id} want to add assoc for word - {word_id_for_assoc}")


@dp.message_handler(state="read_assoc", text="Отчистить все ассоциации🚽")
async def clean_all_assoc(msg: Message, state: FSMContext):
    user = msg.from_user

    await msg.delete()
    async with state.proxy() as data:
        await msg.bot.delete_message(user.id, data.pop("ask_msg_id"))
        word_id_for_assoc = data.pop("word_id_for_assoc")
        learn_words_msg_id = data["learn_words_msg_id"]
    await state.reset_state(with_data=False)

    await db.clean_assoc(word_id_for_assoc)

    await reload_transl_side(word_id_for_assoc, user.id, learn_words_msg_id)

    logging.info(f"For @{user.username}-{user.id} clean all assoc for word {word_id_for_assoc}")


@dp.message_handler(state="read_assoc", text="Отменить↩️")
async def cancel_add_assoc(msg: Message, state: FSMContext):
    user = msg.from_user

    await msg.delete()
    async with state.proxy() as data:
        await msg.bot.delete_message(user.id, data.pop("ask_msg_id"))
        word_id_for_assoc = data.pop("word_id_for_assoc")
    await state.reset_state(with_data=False)

    logging.info(f"For @{user.username}-{user.id} cancel add assoc for word {word_id_for_assoc}")


@dp.message_handler(state="read_assoc")
async def add_assoc(msg: Message, state: FSMContext):
    user = msg.from_user
    assoc = msg.text

    if len(assoc) > 125:
        await msg.answer("Какая-то слишком длинная ассоциация у тебя 🥴\n\n"
                         "Поробуй уложиться в 125 символов:")
        return

    await msg.delete()
    async with state.proxy() as data:
        await msg.bot.delete_message(user.id, data.pop("ask_msg_id"))
        word_id_for_assoc = data.pop("word_id_for_assoc")
        learn_words_msg_id = data["learn_words_msg_id"]
    await state.reset_state(with_data=False)

    new_assoc = await db.update_assoc(word_id_for_assoc, assoc)

    await reload_transl_side(word_id_for_assoc, user.id, learn_words_msg_id)

    logging.info(f"For @{user.username}-{user.id} update assoc in word-{word_id_for_assoc} to -> {new_assoc}")


async def reload_transl_side(word_id: int, user_id: int, learn_words_msg_id: int):
    word = dict(await db.get_transl_side(word_id))
    await bot.edit_message_media(
        InputMediaPhoto(word.pop("transl_img_id"), caption=word.pop("assoc")),
        chat_id=user_id, message_id=learn_words_msg_id,
        reply_markup=keyboards.inline.get_word_menu(word=word, side="word")
    )


