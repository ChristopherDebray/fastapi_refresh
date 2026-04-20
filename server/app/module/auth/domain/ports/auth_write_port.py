from typing import Protocol


class AuthWritePort(Protocol):
    def save_refresh_token(self, user_id: int, refresh_token: str) -> None: ...
