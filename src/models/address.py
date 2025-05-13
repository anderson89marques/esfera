from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address_id: Mapped[str] = mapped_column(index=True) 
    street: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    zipcode: Mapped[str]
    country: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="address")

