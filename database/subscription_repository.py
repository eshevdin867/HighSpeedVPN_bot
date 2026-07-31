import time

import aiosqlite

DB_NAME = "data/users.db"


class SubscriptionRepository:

    async def add(
        self,
        telegram_id: int,
        vpn_client_id: str,
        client_name: str,
        tariff: str,
        days: int,
        expires_at: int
    ):

        async with aiosqlite.connect(DB_NAME) as db:

            await db.execute(
                """
                INSERT INTO subscriptions(

                    telegram_id,
                    vpn_client_id,
                    client_name,
                    tariff,
                    days,
                    expires_at,
                    status,
                    created_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    telegram_id,
                    vpn_client_id,
                    client_name,
                    tariff,
                    days,
                    expires_at,
                    "active",
                    int(time.time())
                )
            )

            await db.commit()

    async def get_by_telegram(
        self,
        telegram_id: int
    ):

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                """
                SELECT *

                FROM subscriptions

                WHERE telegram_id = ?
                """,
                (telegram_id,)
            )

            return await cursor.fetchall()

    async def get_by_client_id(
        self,
        client_id: str
    ):

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                """
                SELECT *

                FROM subscriptions

                WHERE vpn_client_id = ?
                """,
                (client_id,)
            )

            return await cursor.fetchone()

    async def delete(
        self,
        client_id: str
    ):

        async with aiosqlite.connect(DB_NAME) as db:

            await db.execute(
                """
                DELETE

                FROM subscriptions

                WHERE vpn_client_id = ?
                """,
                (client_id,)
            )

            await db.commit()

    async def get_expiring(
        self,
        days_before: int = 3
    ):

        now = int(time.time())

        limit = now + days_before * 86400

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                """
                SELECT *

                FROM subscriptions

                WHERE expires_at <= ?

                AND status = 'active'
                """,
                (limit,)
            )

            return await cursor.fetchall()

    async def get_expired(self):

        now = int(time.time())

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                """
                SELECT *

                FROM subscriptions

                WHERE expires_at < ?

                AND status = 'active'
                """,
                (now,)
            )

            return await cursor.fetchall()


subscription_repo = SubscriptionRepository()
