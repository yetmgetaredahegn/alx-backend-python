#!/usr/bin/python3
import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", results_all)
    print("Users older than 40:", results_older)

# Run concurrent fetch
asyncio.run(fetch_concurrently())

