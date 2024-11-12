from pydantic import BaseModel


class BaseTask(BaseModel):
    title: str


class CreateTask(BaseTask):
    user_id: int
