from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from auth.models import Base
from config import settings
from utils.logger import logger


async def init_database():
    """Initialize the database with all tables."""
    try:
        # Create async engine
        engine = create_async_engine(settings.database_url, echo=settings.debug)
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
        # Close engine
        await engine.dispose()
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_database_session() -> AsyncSession:
    """Get a database session."""
    engine = create_async_engine(settings.database_url, echo=settings.debug)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_database()) 