import logging

import asyncpg
from asyncpg import Pool

from data import config


class Database:
    def __init__(self, pool: Pool) -> None:
        self.pool: Pool = pool


    @classmethod
    async def create(cls):
        logging.info("Connect to Database")

        pool = await asyncpg.create_pool(
            user=config.PG_USER,
            password=config.PG_PASSWORD,
            database=config.PG_DB,
            host=config.IP
        )
        return cls(pool)

    async def create_all_tables_ine(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS Users(
                id integer PRIMARY KEY,
                username varchar(64) not null,
                full_name varchar(64) not null,
                connected_user_ids integer[] not null
            );
            
            CREATE TABLE IF NOT EXISTS Sets(
                id serial primary key,
                user_id integer not null references Users(id) on delete cascade,
                name varchar(50) not null,
                public_date date default now()
            );
            CREATE INDEX IF NOT EXISTS user_for_sets_idx ON Sets(user_id);
            ALTER DATABASE {config.PG_DB} SET timezone TO 'Europe/Kiev';
            
            CREATE TABLE IF NOT EXISTS Words(
                id serial primary key,
                set_id integer not null references Sets(id) on delete cascade,
                assoc text,
                word_photo_id integer not null,
                translation_photo_id integer not null,
                base_photo_id integer not null
            );
            CREATE INDEX IF NOT EXISTS set_for_words_idx ON Words(set_id);
        """
        await self.pool.execute(sql)


    async def add_set(self, **data) -> int:
        columns = ", ".join(data.keys())
        nums = ", ".join(
            [f"${num}" for num in range(1, len(data)+1)]
        )

        sql = f"""
            INSERT INTO Sets({columns}) VALUES ({nums})
                RETURNING id;
        """
        set_id = await self.pool.fetchval(sql, *data.values())

        logging.info(f"Add new set #{set_id} -> {data}")

        return set_id


    async def add_word(self, set_id, **data):
        columns = ", ".join(data.keys())
        nums = ", ".join(
            [f"${num}" for num in range(1, len(data) + 1)]
        )

        sql = f"""
            INSERT INTO Words({columns}) VALUES ({nums});
        """

        await self.pool.execute(sql, *data.values())


    async def add_user(self, **data):
        columns = ", ".join(data.keys())
        nums = ", ".join(
            [f"${num}" for num in range(1, len(data) + 1)]
        )

        sql = f"""
                    INSERT INTO Users({columns}) VALUES ({nums});
                """

        data.update(connected_user_ids=[data['id']])
        logging.info(f"Add new user @{data['username']}-{data['id']}")

        await self.pool.execute(sql, *data.values())


    async def add_connecting_user(self, user_id: int, connecting_user_id: int):
        sql = """
            UPDATE Users
                SET connected_user_ids = array_append(connected_user_ids, $2)
                    WHERE id = $1;
        """

        logging.info(f"Add connecting User-{connecting_user_id} for User-{user_id}")

        await self.pool.execute(sql, user_id, connecting_user_id)


    async def get_sets(self, user_id: int, page: int) -> list:
        offset = (page-1) * 10
        sql = """
            SELECT id, name FROM Sets
                WHERE user_id in (SELECT connected_user_ids FROM Users WHERE id=$1)
                    ORDER BY public_date DESC
                        LIMIT 10 OFFSET $2;
        """

        sets = await self.pool.fetch(sql, user_id, offset)

        logging.info(f"For {user_id} get sets -> {sets} on page {page}")

        return sets


    async def get_words_by_set_id(self, set_id: int) -> list:
        sql = """
            SELECT * FROM Words
                WHERE set_id=$1;
        """

        logging.info(f"Get words in set-{set_id} for user")

        return await self.pool.fetch(sql, set_id)


    async def is_user_exists(self, user_id: int) -> bool:
        sql = """
            SELECT True as is_exists FROM Users WHERE id = $1;
        """
        is_exists = True if await self.pool.fetchrow(sql, user_id) else False

        logging.info(f"Is user-{user_id} exist --- {is_exists}")

        return is_exists
