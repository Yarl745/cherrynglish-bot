from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from keyboards.inline.sets_menu import sets_menu_callback
from loader import dp


@dp.callback_query_handler(sets_menu_callback.filter(action="next_page"))
async def get_next_page(call: CallbackQuery, state: FSMContext):
    msg = call.message
    user = call.from_user

    async with state.proxy() as data:
        data["page"] += 1
        page = data["page"]

    await msg.edit_reply_markup(reply_markup=await keyboards.inline.get_sets_menu(user.id, page))

    await call.answer("Страница №{}".format(page))


@dp.callback_query_handler(sets_menu_callback.filter(action="previous_page"))
async def get_next_page(call: CallbackQuery, state: FSMContext):
    msg = call.message
    user = call.from_user

    async with state.proxy() as data:
        data["page"] -= 1
        page = data["page"]

    await msg.edit_reply_markup(reply_markup=await keyboards.inline.get_sets_menu(user.id, page))

    await call.answer("Страница №{}".format(page))

