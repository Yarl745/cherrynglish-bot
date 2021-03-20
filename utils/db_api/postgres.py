import logging
import random

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
        sql = """
            CREATE TABLE IF NOT EXISTS Users(
                id integer PRIMARY KEY,
                username varchar(64) not null,
                full_name varchar(64) not null,
                connected_user_ids integer[] default '{}' 
            );
            
            CREATE TABLE IF NOT EXISTS Sets(
                id serial primary key,
                user_id integer not null references Users(id) on delete cascade,
                name varchar(50) not null,
                public_timestamp timestamp default now()
            );
            CREATE INDEX IF NOT EXISTS user_for_sets_idx ON Sets(user_id);
            
            CREATE TABLE IF NOT EXISTS Words(
                id serial primary key,
                set_id integer not null references Sets(id) on delete cascade,
                assoc text DEFAULT ' ',
                word_img_id varchar(120) not null,
                transl_img_id varchar(120) not null,
                base_img_id varchar(120) not null
            );
            CREATE INDEX IF NOT EXISTS set_for_words_idx ON Words(set_id);
            
            CREATE TABLE IF NOT EXISTS Repeats(
                set_id integer not null references Sets(id) on delete cascade,
                user_id integer not null,
                set_name varchar(50) not null,
                repeat_time timestamp not null,
                repeat_stage smallint not null default 0,
                PRIMARY KEY (set_id, user_id)
            );      
        """
        await self.pool.execute(sql)

        logging.info(f"Create all tables (if not exist)")


    async def get_repeat(self, user_id: int, set_id: int) -> dict:
        sql = """
            SELECT repeat_stage, repeat_time FROM Repeats
                WHERE user_id=$1 AND set_id=$2
                    LIMIT 1;
        """
        repeat = await self.pool.fetchrow(sql, user_id, set_id)
        logging.info(f"Get repeat [{repeat}] for User-{user_id} on the set-{set_id}")
        return repeat


    async def get_all_repeats(self) -> list:
        sql = """
            SELECT * FROM Repeats;
        """
        repeats = await self.pool.fetch(sql)
        logging.info(f"Get all repeats [{repeats}]")
        return repeats


    async def update_repeat(self, user_id: int, set_id: int, **data):
        values = ", ".join([f"{key}=${num}" for num, key in enumerate(data, start=3)])
        sql = f"""
            UPDATE Repeats
                SET {values}
                    WHERE user_id=$1 and set_id=$2;
        """
        await self.pool.execute(sql, user_id, set_id, *data.values())
        logging.info(f"For User-{user_id} on the set-{set_id} update repeat data -> [{data}]")


    async def add_repeat(self, **data):
        user_id = data["user_id"]
        set_id = data["set_id"]

        columns = ", ".join(data.keys())
        nums = ", ".join(
            [f"${num}" for num in range(1, len(data)+1)]
        )

        sql = f"""
            INSERT INTO Repeats({columns}) VALUES ({nums});
        """
        await self.pool.execute(sql, *data.values())
        logging.info(f"For User-{user_id} on the set-{set_id} add repeat data -> [{data}]")


    async def clean_assoc(self, word_id: int):
        sql = """
            UPDATE Words
                SET assoc = ' '
                    WHERE id = $1;  
        """
        await self.pool.execute(sql, word_id)
        logging.info(f"Clean all assoc in word {word_id}")


    async def update_assoc(self, word_id: int, assoc: str):
        sql = """
            UPDATE Words
                SET assoc = concat(assoc, '\n\n', $2::text) 
                    WHERE id = $1
                        RETURNING assoc; 
        """
        new_assoc = await self.pool.fetchval(sql, word_id, assoc)
        logging.info(f"Add assoc [{assoc}] for word {word_id}")
        return new_assoc


    async def config_timezone(self):
        await self.pool.execute(f"ALTER DATABASE {config.PG_DB} SET timezone TO 'Europe/Kiev';")
        logging.info(f"Config timezone")


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


    async def add_word(self, **data):
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
                    INSERT INTO Users({columns}) VALUES ({nums})
                        ON CONFLICT DO NOTHING;
        """

        logging.info(f"Add new user @{data['username']}-{data['id']}")

        await self.pool.execute(sql, *data.values())


    async def is_users_connected(self, user_id: int, connected_user_id: int):
        sql = """
               SELECT array_position(connected_user_ids, $2) FROM Users WHERE id = $1;
           """

        is_connected = True if await self.pool.fetchval(sql, user_id, connected_user_id) else False
        logging.info(f"Check User-{connected_user_id} already connected to User-{user_id} --- {is_connected}")

        return is_connected


    async def add_connected_user(self, user_id: int, connected_user_id: int):
        sql = """
            UPDATE Users
                SET connected_user_ids = array_append(connected_user_ids, $2)
                    WHERE id = $1;
        """

        logging.info(f"Add connecting User-{connected_user_id} for User-{user_id}")

        await self.pool.execute(sql, user_id, connected_user_id)


    async def get_connected_users(self, user_id: int):
        sql = """
            SELECT id, full_name, username FROM Users
                WHERE id IN (SELECT unnest(connected_user_ids) FROM Users WHERE id=$1);
        """
        connected_users: list = await self.pool.fetch(sql, user_id)

        logging.info(f"For user-{user_id} get connected_user -- {connected_users}")

        return connected_users


    async def del_connected_user(self, user_id: int, connected_user_id: int):
        sql = """
            UPDATE Users
                SET connected_user_ids = array_remove(connected_user_ids, $2)
                    WHERE id = $1;
        """

        await self.pool.execute(sql, user_id, connected_user_id)

        logging.info(f"For user-{user_id} delete connected_user_id {connected_user_id}")


    async def get_set_name(self, set_id: int) -> str:
        sql = """
            SELECT name FROM Sets WHERE id=$1 LIMIT 1;
        """

        set_name = await self.pool.fetchval(sql, set_id)

        logging.info(f"Get set_name[{set_name}] for set-{set_id}")

        return set_name


    async def get_sets(self, user_id: int, page: int) -> list:
        page = 1 if page < 1 else page
        offset = (page-1) * 10
        sql = """
            SELECT id, name FROM Sets
                WHERE user_id in (SELECT unnest(connected_user_ids) FROM Users WHERE id=$1) OR user_id=$1
                    ORDER BY public_timestamp DESC
                        LIMIT 10 OFFSET $2;
        """

        sets = await self.pool.fetch(sql, user_id, offset)

        logging.info(f"For {user_id} get sets -> {sets} on page {page}")

        return sets


    async def get_word_side(self, word_id: int) -> dict:
        sql = """
            SELECT id as word_id, set_id, word_img_id FROM Words
                WHERE id = $1 LIMIT 1;
        """
        word_side = await self.pool.fetchrow(sql, word_id)
        return word_side


    async def get_transl_side(self, word_id: int) -> dict:
        sql = """
            SELECT id as word_id, set_id, transl_img_id, assoc FROM Words
                WHERE id = $1 LIMIT 1;
        """
        transl_side = await self.pool.fetchrow(sql, word_id)
        return transl_side


    async def get_shuffled_word_ids(self, set_id: int) -> list:
        sql = """
            SELECT id as word_id FROM Words WHERE set_id=$1;
        """

        word_ids = await self.pool.fetch(sql, set_id)
        random.shuffle(word_ids)

        logging.info(f"Get word_ids-{word_ids} in set-{set_id} for user")

        return word_ids