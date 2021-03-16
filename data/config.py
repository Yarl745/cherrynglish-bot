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


EXAMPLE_IMGS = (
    "AgACAgIAAxkBAANHYE3U7lJcgbf1U0O9ylGGBeOuZ3YAAgayMRuI1HFKLtjiqSTIcgeoZ4meLgADAQADAgADeQADP8UDAAEeBA",
    "AgACAgIAAxkBAANJYE3U9uDsrNZpza-od4sfY4AihI8AAgOyMRuI1HFK4JvEfAyW9q-h0Q-bLgADAQADAgADeQADCgQEAAEeBA",
    "AgACAgIAAxkBAANNYE3VZ5BG0B6UgKrh2sFqOjdDtDAAAgmyMRuI1HFK8bYL4g_sQ2NoZomeLgADAQADAgADeQADjMwDAAEeBA"
)


HELPER_CHANNEL_ID = -1001316268421