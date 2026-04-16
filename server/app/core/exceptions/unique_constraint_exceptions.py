class UniqueConstraintException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"{field} '{value}' already exists")
