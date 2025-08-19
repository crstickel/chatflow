
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any

from app.dependencies import get_engine, AppDependencyCollection
from app.dto.auth import LoginResponseDTO, RegisterRequestDTO
from app.dto.user import PublicUserDTO
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=LoginResponseDTO)
async def login(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    token = AuthService(app_engine).login_user(
        username=form_data.username,
        password=form_data.password
    )

    if token is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="invalid username or password")

    return LoginResponseDTO(
        access_token=token.id,
        token_type='bearer',
        expires_in=token.time_to_live
    )


@router.post('/register', response_model=PublicUserDTO)
async def login(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
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

