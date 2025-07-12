import aiosqlite
import asyncio

DB_NAME = "users.db"


async def create_and_seed_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        await db.execute("DELETE FROM users;")  # نفرّغ الجدول للتجربة
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?);", [
            ("Alice", 25),
            ("Bob", 45),
            ("Charlie", 35),
            ("David", 60)
        ])
        await db.commit()

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
    asyncio.run(create_and_seed_db())
