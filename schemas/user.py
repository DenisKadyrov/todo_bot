from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str | None = None
    
class CreateUser(BaseUser):
    id: int
    chat_id: str
