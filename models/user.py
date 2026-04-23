from sqlalchemy.types import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str | None] = mapped_column(nullable=True)
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
    )
