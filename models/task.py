from sqlalchemy import ForeignKey
from sqlalchemy.types import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship('User', back_populates='tasks')

