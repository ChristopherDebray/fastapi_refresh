from typing import Protocol

from app.module.auth.infrastructure.dtos.outputs import AuthUserWithPasswordDto


class AuthReadPort(Protocol):
    def find_by_email(self, email: str) -> AuthUserWithPasswordDto | None: ...
