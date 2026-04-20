from typing import Protocol


class AuthWritePort(Protocol):
    def save_refresh_token(self, user_id: int, refresh_token: str | None) -> None:
        """
        Sauvegarde ou supprime le refresh token d'un utilisateur

        Args:
            user_id: ID de l'utilisateur
            refresh_token: Token à sauvegarder, ou None pour supprimer
        """
        pass
