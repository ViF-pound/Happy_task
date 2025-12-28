import datetime

from typing import TYPE_CHECKING
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
if TYPE_CHECKING:
    from src.models.task_model import Task


class User(Base):
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    user_name:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    created_at:Mapped[datetime.date] = mapped_column(Date)

    tasks:Mapped[list["Task"]] = relationship(back_populates="user", uselist=True)
