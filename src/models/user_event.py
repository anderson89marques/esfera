from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class UserEvent(Base):
    __tablename__ = "user_events"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(index=True)
    event_timestamp: Mapped[datetime]

