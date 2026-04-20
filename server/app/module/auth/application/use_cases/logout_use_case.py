from app.core.security.token_payload import TokenPayloadDto
from app.module.auth.domain.ports.auth_write_port import AuthWritePort


class LogoutUseCase:
    def __init__(self, write_repo: AuthWritePort):
        self.write_repo = write_repo

    def execute(self, current_user: TokenPayloadDto) -> None:
        self.write_repo.save_refresh_token(current_user.id, None)
