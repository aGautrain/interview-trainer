"""
Database connection and query utilities for the Interview Trainer API.

This module handles:
- Database connection pool management
- Query execution utilities
- Database initialization
"""

import os
import asyncpg
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'interview_trainer'),
    'user': os.getenv('DB_USER', 'interview_user'),
    'password': os.getenv('DB_PASSWORD', 'interview_password'),
    'min_size': 5,
    'max_size': 20
}

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def init_db():
    """Initialize the database connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(**DB_CONFIG)
    return _pool


async def close_db():
    """Close the database connection pool"""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def get_db_connection():
    """Get a database connection from the pool"""
    if _pool is None:
        await init_db()
    
    async with _pool.acquire() as connection:
        yield connection


async def fetch_one(query: str, *args) -> Optional[Dict[str, Any]]:
    """Execute a query and return a single row as a dictionary"""
    async with get_db_connection() as conn:
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None


async def fetch_all(query: str, *args) -> List[Dict[str, Any]]:
    """Execute a query and return all rows as a list of dictionaries"""
    async with get_db_connection() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(row) for row in rows]


async def execute(query: str, *args) -> str:
    """Execute a query that doesn't return data (INSERT, UPDATE, DELETE)"""
    async with get_db_connection() as conn:
        return await conn.execute(query, *args)


async def fetch_val(query: str, *args) -> Any:
    """Execute a query and return a single value"""
    async with get_db_connection() as conn:
        return await conn.fetchval(query, *args)


async def execute_transaction(queries: List[tuple]) -> List[Any]:
    """
    Execute multiple queries in a single transaction.
    
    Args:
        queries: List of tuples where each tuple is (query_string, *args)
        
    Returns:
        List of results from each query
        
    Raises:
        Exception: If any query fails, the entire transaction is rolled back
    """
    async with get_db_connection() as conn:
        async with conn.transaction():
            results = []
            for query_info in queries:
                if len(query_info) == 1:
                    query = query_info[0]
                    args = ()
                else:
                    query = query_info[0]
                    args = query_info[1:]
                
                # Determine query type and execute appropriately
                query_lower = query.strip().lower()
                if query_lower.startswith(('select',)):
                    if 'limit 1' in query_lower or 'fetch_one' in query.lower():
                        result = await conn.fetchrow(query, *args)
                        results.append(dict(result) if result else None)
                    else:
                        rows = await conn.fetch(query, *args)
                        results.append([dict(row) for row in rows])
                elif query_lower.startswith(('insert', 'update', 'delete')):
                    if 'returning' in query_lower:
                        result = await conn.fetchrow(query, *args)
                        results.append(dict(result) if result else None)
                    else:
                        result = await conn.execute(query, *args)
                        results.append(result)
                else:
                    # Default to fetchval for other queries
                    result = await conn.fetchval(query, *args)
                    results.append(result)
            
            return results