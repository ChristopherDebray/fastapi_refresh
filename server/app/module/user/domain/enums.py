import enum


class UserRole(enum.StrEnum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    DRIVER = "DRIVER"
    OPERATOR = "OPERATOR"


class UserStatus(enum.StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
