from app.database.models import async_session
from app.database.models import User, Category, SupportRequest
from sqlalchemy import select


async def set_user(tg_id: int, name: str, phone_number: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, name=name, phone_number=phone_number)
            session.add(new_user)
            await session.commit()


async def create_support_request(user_tg_id: int, category_id: int, description: str) -> None:
    async with async_session() as session:

        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))

        if user:

            category = await session.scalar(select(Category).where(Category.id == category_id))

            if category:

                support_request = SupportRequest(
                    user_id=user.id,
                    category_id=category.id,
                    description=description
                )
                session.add(support_request)
                await session.commit()
            else:
                raise ValueError("Категория не найдена")
        else:
            raise ValueError("Пользователь не найден")


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
