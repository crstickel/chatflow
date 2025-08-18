
from fastapi import APIRouter
from typing import Any

from app.dependencies import CurrentUserDependency
from app.dto.user import PublicUserDTO

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/me', response_model=PublicUserDTO)
async def get_my_info(
    current_user: CurrentUserDependency
) -> Any:
    return current_user

