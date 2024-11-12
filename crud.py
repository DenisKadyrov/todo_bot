import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base, Task, User


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

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
        user_id: str
    ) -> List[ModelType]:
        stmt = select(self.model).where(self.model.user_id==user_id)
        return await db.scalars(stmt)

    async def remove(self, db: AsyncSession, id: int) -> None:
        await db.execute(delete(self.model).where(self.model.id == int(id)))
        await db.flush()


class CRUDUser(CRUDBase):
    pass

task_crud = CRUDTask(Task)
user_crud = CRUDUser(User)
