# backend/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, Product, Order

class UserRepository:
    @staticmethod
    async def get_user_by_tg_id(db: AsyncSession, tg_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == tg_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def upsert_user(db: AsyncSession, tg_id: int, username: str) -> User:
        user = await UserRepository.get_user_by_tg_id(db, tg_id)
        if user:
            user.username = username
        else:
            user = User(telegram_id=tg_id, username=username)
            db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

class ProductRepository:
    @staticmethod
    async def list_products(db: AsyncSession):
        stmt = select(Product)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        return result.scalars().first()

class OrderRepository:
    @staticmethod
    async def create_order(db: AsyncSession, user_id: int, product_id: int) -> Order:
        order = Order(user_id=user_id, product_id=product_id, status="created")
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def update_order_status(db: AsyncSession, order_id: int, new_status: str) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = await db.execute(stmt)
        order = result.scalars().first()
        if order:
            order.status = new_status
            await db.commit()
            await db.refresh(order)
            return order
        return None
