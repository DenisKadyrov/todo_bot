from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base, Task, User


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        return await db.scalar(stmt)

    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType
    ) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class CRUDTask(CRUDBase):
    async def get_multi(
        self, 
        db: AsyncSession,
        user_id: int,
    ) -> list[Task]:
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.id)
        )
        return list(await db.scalars(stmt))

    async def remove(
        self,
        db: AsyncSession,
        id: int,
        user_id: int | None = None,
    ) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id == user_id)

        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0


class CRUDUser(CRUDBase):
    pass

task_crud = CRUDTask(Task)
user_crud = CRUDUser(User)
