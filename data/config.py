from datetime import timedelta

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста


PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_DB = env.str("PG_DB")
PG_PORT = env.str("PG_PORT")
PG_HOST = env.str("PG_HOST")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")


EXAMPLE_IMGS = (
    "AgACAgIAAxkBAANHYE3U7lJcgbf1U0O9ylGGBeOuZ3YAAgayMRuI1HFKLtjiqSTIcgeoZ4meLgADAQADAgADeQADP8UDAAEeBA",
    "AgACAgIAAxkBAANJYE3U9uDsrNZpza-od4sfY4AihI8AAgOyMRuI1HFK4JvEfAyW9q-h0Q-bLgADAQADAgADeQADCgQEAAEeBA",
    "AgACAgIAAxkBAANNYE3VZ5BG0B6UgKrh2sFqOjdDtDAAAgmyMRuI1HFK8bYL4g_sQ2NoZomeLgADAQADAgADeQADjMwDAAEeBA"
)


repeat_stages = [
    timedelta(minutes=30), timedelta(hours=1), timedelta(hours=3),
    timedelta(days=1), timedelta(days=2), timedelta(days=4),
    timedelta(days=8), timedelta(days=14), timedelta(days=30),
    timedelta(days=90), timedelta(days=180), timedelta(days=360),
    timedelta(days=720)
]