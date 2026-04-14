import enum

class UserRole(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    DRIVER = "DRIVER"
    OPERATOR = "OPERATOR"

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"