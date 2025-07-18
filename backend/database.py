from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from auth.models import Base
from config import settings
from utils.logger import logger


async def init_database():
    """Initialize the database with all tables."""
    try:
        # Convert PostgreSQL URL to async format
        if settings.database_url.startswith('postgresql://'):
            async_url = settings.database_url.replace('postgresql://', 'postgresql+asyncpg://')
        else:
            async_url = settings.database_url
        
        logger.info(f"Initializing database with URL: {async_url}")
        
        # Create async engine
        engine = create_async_engine(async_url, echo=settings.debug)
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
        # Close engine
        await engine.dispose()
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_database_session():
    """Get a database session."""
    try:
        # Convert PostgreSQL URL to async format
        if settings.database_url.startswith('postgresql://'):
            async_url = settings.database_url.replace('postgresql://', 'postgresql+asyncpg://')
        else:
            async_url = settings.database_url
        
        engine = create_async_engine(async_url, echo=settings.debug)
        AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_database()) 