import aiosqlite

DB_NAME = "data/users.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS support_messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_message_id INTEGER UNIQUE,
                user_id INTEGER
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================
        # Подписки VPN
        # =====================================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id INTEGER NOT NULL,

            vpn_client_id TEXT NOT NULL UNIQUE,

            client_name TEXT NOT NULL,

            tariff TEXT NOT NULL,

            days INTEGER NOT NULL,

            expires_at INTEGER NOT NULL,

            status TEXT NOT NULL DEFAULT 'active',

            created_at INTEGER NOT NULL

        )
        """)

        await db.commit()


async def user_exists(telegram_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT 1 FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        user = await cursor.fetchone()
        return user is not None


async def add_user(telegram_id: int, username: str, first_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO users
            (telegram_id, username, first_name)
            VALUES (?, ?, ?)
            """,
            (telegram_id, username, first_name)
        )
        await db.commit()


async def save_support_message(
        admin_message_id: int,
        user_id: int
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO support_messages
            (admin_message_id, user_id)
            VALUES (?, ?)
            """,
            (
                admin_message_id,
                user_id
            )
        )

        await db.commit()

async def get_user_by_admin_message(
        admin_message_id: int
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT user_id
            FROM support_messages
            WHERE admin_message_id = ?
            """,
            (admin_message_id,)
        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return None


async def get_all_users():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT telegram_id
            FROM users
            """
        )

        users = await cursor.fetchall()

        return [
            user[0]
            for user in users
        ]

async def add_news(text: str):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO news(text)
            VALUES(?)
            """,
            (text,)
        )

        await db.commit()


async def get_last_news():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT text
            FROM news
            ORDER BY id DESC
            LIMIT 1
            """
        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return None
