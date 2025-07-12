import aiosqlite
import asyncio

DB_NAME = "users.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users;")
        users = await cursor.fetchall()
        print("👤 All Users:")
        for user in users:
            print(user)

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40;")
        older_users = await cursor.fetchall()
        print("\n🎯 Users Older Than 40:")
        for user in older_users:
            print(user)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
