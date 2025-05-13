from datetime import datetime 
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(index=True)
    name: Mapped[str]
    created_at: Mapped[datetime] 
    email: Mapped[str]
    address = relationship("Address", back_populates="user")


