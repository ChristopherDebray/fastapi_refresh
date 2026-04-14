from app.core.security.encrypt_service import EncryptService
from app.module.user.domain.enums import UserRole, UserStatus

default_password = EncryptService.hash("test1234")

USERS = [
    {
        "email": "superadmin@example.com",
        "first_name": "Superadmin",
        "last_name": "User",
        "password": default_password,
        "role": UserRole.SUPERADMIN,
        "status": UserStatus.ACTIVE,
    },
    {
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "password": default_password,
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
    },
    {
        "email": "supervisor@example.com",
        "first_name": "Supervisor",
        "last_name": "User",
        "password": default_password,
        "role": UserRole.SUPERVISOR,
        "status": UserStatus.ACTIVE,
    },
    {
        "email": "driver@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": default_password,
        "role": UserRole.DRIVER,
        "status": UserStatus.ACTIVE,
    },
    {
        "email": "operator@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": default_password,
        "role": UserRole.OPERATOR,
        "status": UserStatus.ACTIVE,
    },
]