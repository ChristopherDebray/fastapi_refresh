from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.module.user.domain.enums import UserRole, UserStatus

class UserModel(Base):
    __tablename__ = "fpi_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(55))
    last_name: Mapped[str] = mapped_column(String(55))
    password: Mapped[str] = mapped_column(String(255))
    # `server_default` is used to have the default value inside the database / migration,
    # `default` is only for the sql alchemy object creation
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.OPERATOR, server_default=UserRole.OPERATOR.value)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.ACTIVE, server_default=UserStatus.ACTIVE.value)