# src/services/memory_service.py
import asyncpg
from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import asyncio

class MemoryService:
    def __init__(self):
        self.pool = None
        # Run async initialization in the event loop
        asyncio.create_task(self.init_pool_and_db())

    async def init_pool_and_db(self):
        """Initializes the connection pool and the database table."""
        try:
            self.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME
            )
            await self._check_and_init_db()
        except Exception as e:
            print(f"Database connection pool failed: {e}")

    async def _check_and_init_db(self):
        """Checks if the 'memories' table exists and creates it if not."""
        if not self.pool: return
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)

    async def add_memory(self, text: str):
        """Adds a new memory to the database asynchronously."""
        if not self.pool: return
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO memories (content) VALUES ($1);", text)

    async def retrieve_relevant_memories(self, query_text: str, limit: int = 5):
        """Retrieves memories relevant to the query text asynchronously."""
        if not self.pool: return []

        keywords = query_text.split()
        if not keywords: return []

        async with self.pool.acquire() as conn:
            # Building a simple ILIKE query for keyword matching
            query_conditions = [f"content ILIKE ${i+1}" for i in range(len(keywords))]
            query = f"SELECT content FROM memories WHERE {' OR '.join(query_conditions)} ORDER BY created_at DESC LIMIT ${len(keywords) + 1};"

            # Add wildcards to keywords for partial matching
            like_keywords = [f"%{keyword}%" for keyword in keywords]

            rows = await conn.fetch(query, *like_keywords, limit)
            return [row['content'] for row in rows]

# Singleton instance for the application
memory_service = MemoryService()
