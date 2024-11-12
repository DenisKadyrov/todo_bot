from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    
class CreateUser(BaseUser):
    id: int
    chat_id: str
    username: str

