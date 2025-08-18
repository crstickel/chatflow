
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any

from app.dependencies import engine, AppDependencyCollection
from app.dto.auth import LoginResponseDTO, RegisterRequestDTO
from app.dto.user import PublicUserDTO
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=LoginResponseDTO)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    raise NotImplementedError()


@router.post('/register', response_model=PublicUserDTO)
async def login(
    app_engine: Annotated[AppDependencyCollection, Depends(engine)],
    form_data: RegisterRequestDTO
) -> Any:
    try:
        user = AuthService(app_engine).register_new_user(
            username=form_data.username,
            email=form_data.email,
            password=form_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.args[0]))

