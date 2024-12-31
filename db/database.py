import asyncpg
from asyncpg import Pool
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            min_size=5,
            max_size=20
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        if not self.pool:
            raise Exception("Database not connected")
        return await self.pool.execute(query, *args)

    async def fetch(self, query: str, *args):
        if not self.pool:
            raise Exception("Database not connected")
        return await self.pool.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        if not self.pool:
            raise Exception("Database not connected")
        return await self.pool.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        if not self.pool:
            raise Exception("Database not connected")
        return await self.pool.fetchval(query, *args)

database = Database()

async def init_db():
    await database.connect()
    # Create tables if they don't exist
    await database.execute("""
        CREATE TABLE IF NOT EXISTS scraping_jobs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            url TEXT NOT NULL,
            schedule TEXT,
            format TEXT CHECK (format IN ('json', 'csv')),
            status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed')),
            configuration JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            result_location TEXT,
            error_message TEXT
        );
    """)
    await database.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            data_id UUID REFERENCES scraping_jobs(id),
            analysis_type TEXT NOT NULL,
            parameters JSONB,
            result JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            processing_time INTERVAL,
            status TEXT CHECK (status IN ('pending', 'completed', 'failed')),
            error_message TEXT
        );
    """)
