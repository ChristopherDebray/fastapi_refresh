from fastapi import APIRouter, Depends, status

from app.module.user.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.module.user.application.use_cases.get_user_use_case import GetUserUseCase
from app.module.user.application.use_cases.get_users_use_case import GetUsersUseCase
from app.module.user.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.module.user.infrastructure.dtos.outputs import UserResponseDto
from app.module.user.infrastructure.dtos.inputs import UserCreateDto, UserUpdateDto
from app.module.user.application.use_cases.create_user_use_case import CreateUserUseCase
from app.module.user.presentation.dependancies import get_create_user_use_case, get_delete_user_use_case, get_get_user_use_case, get_get_users_use_case, get_update_user_use_case

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=list[UserResponseDto], status_code=status.HTTP_200_OK)
def get_users(use_case: GetUsersUseCase = Depends(get_get_users_use_case)) -> list[UserResponseDto]:
    return use_case.execute();

@router.get("/{user_id}", response_model=UserResponseDto | None, status_code=status.HTTP_200_OK)
def get_user(user_id: int, use_case: GetUserUseCase = Depends(get_get_user_use_case)) -> UserResponseDto:
    return use_case.execute(user_id)

@router.post("", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateDto, use_case: CreateUserUseCase = Depends(get_create_user_use_case)) -> UserResponseDto:
    return use_case.execute(payload)

@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    payload: UserUpdateDto,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case)
) -> UserResponseDto:
    return use_case.execute(user_id, payload)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, use_case: DeleteUserUseCase = Depends(get_delete_user_use_case)) -> None:
    return use_case.execute(user_id)