import os

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base

pytest_plugins = [
    'tests.fixtures.user',
]


@pytest_asyncio.fixture(autouse=True, name='session')
async def init_db():
    engine = create_async_engine(
        os.getenv('DB_TEST_URL')
    )
    TestingSessionLocal = sessionmaker(
        class_=AsyncSession, bind=engine, expire_on_commit=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:  # noqa
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
