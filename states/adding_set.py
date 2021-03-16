from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingSet(StatesGroup):
    read_photos = State()
    read_set_name = State()
    config_sizes = State()
    loading_data = State()
