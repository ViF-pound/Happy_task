import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey

from src.db import Base
from src.models.user_model import User


class Task(Base):
    __tablename__ = "task_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]
    text:Mapped[str]
    created_at:Mapped[datetime.date] = mapped_column(Date)
    updated_at:Mapped[datetime.date] = mapped_column(Date, nullable=True)

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user:Mapped["User"] = relationship(back_populates="tasks", uselist=False)