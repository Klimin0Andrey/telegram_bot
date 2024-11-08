from config import DB_URL
from sqlalchemy import BigInteger, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)

    requests: Mapped[list["SupportRequest"]] = relationship("SupportRequest", back_populates="user")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)

    requests: Mapped[list["SupportRequest"]] = relationship("SupportRequest", back_populates="category")


class SupportRequest(Base):
    __tablename__ = 'support_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="ожидание")

    user: Mapped["User"] = relationship("User", back_populates="requests")
    category: Mapped["Category"] = relationship("Category", back_populates="requests")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as session:
        cat1 = Category(name="Разработка корпоративных приложений",
                        description='Создание приложений для управления внутренними бизнес-процессами.')
        cat2 = Category(name="Системы контроля за сотрудниками",
                        description='Решения для мониторинга и повышения эффективности работы сотрудников.')
        cat3 = Category(name="Системы лояльности и бонусов",
                        description='Разработка программ для удержания клиентов с бонусами и скидками.')
        cat4 = Category(name="Разработка сайтов", description='Создание и поддержка веб-сайтов для бизнеса.')
        cat5 = Category(name="Приложения для карт и бонусов",
                        description='Разработка приложений для карт лояльности и учета бонусов.')
        cat6 = Category(name="Другое", description='Специализированные решения под индивидуальные требования бизнеса.')
        session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
        await session.commit()


async def main():
    await async_main()
    await insert_data()
