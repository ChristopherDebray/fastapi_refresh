from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class User(Base):
    __tablename__ = "fpi_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(55))
    last_name: Mapped[str] = mapped_column(String(55))