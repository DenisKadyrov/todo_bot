from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[list["Taks"]] = relationship('Task', back_populates='user')

