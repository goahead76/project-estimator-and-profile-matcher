from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.config import DATABASE_URL

# async engine for high-performance pooling
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_= AsyncSession,
    expire_on_commit = False
)

Base = declarative_base()

#ORM model for DB
class user(Base):
    __tablename__ = "estimator"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default= datetime.utcnow)

#dependency to inject DB sesson to API endpoints(safely)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise