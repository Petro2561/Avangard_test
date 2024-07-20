from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    coins = relationship("Coin", back_populates="user")


class Coin(Base):
    __tablename__ = "coin"
    id = Column(Integer, primary_key=True)
    coin_name = Column(String, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="coins")


DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
