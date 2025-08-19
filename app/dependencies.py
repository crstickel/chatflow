
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from functools import cached_property
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlmodel import create_engine, Session
from typing import Annotated, Self

from app.config import settings
from app.repositories.accesstoken import AccessTokenRepository, DbAccessTokenRepository
from app.repositories.conversation import ConversationRepository, DbConversationRepository
from app.repositories.membership import MembershipRepository, DbMembershipRepository
from app.repositories.user import UserRepository, DbUserRepository
from app.models.user import User

from shared.time import get_current_time


###################################################################################################
#
#   Application Dependency Collections
#
###################################################################################################

class AppDependencyCollection:

    def __init__(self, session: Session):
        self.session = session


    @cached_property
    def conversation_repository(self) -> ConversationRepository:
        return DbConversationRepository(self.session)


    @cached_property
    def membership_repository(self) -> MembershipRepository:
        return DbMembershipRepository(self.session)


    @cached_property
    def token_repository(self) -> AccessTokenRepository:
        return DbAccessTokenRepository(self.session)


    @cached_property
    def user_repository(self) -> UserRepository:
        return DbUserRepository(self.session)


    def __call__(self) -> Self:
        '''
        Dunder/magic method which allows the instance itself to be called, which provides
        compatibility with FastAPI's dependency injection system via Depends(..)
        '''

        return self



###################################################################################################
#
#   FastAPI Dependency-Injected Helpers
#
###################################################################################################

db_engine = create_engine(settings.DB_URL)
SessionFactory = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)

def get_engine():
    '''
    Retrieves the current application dependency container (aka "engine")
    '''
    session = SessionFactory()
    try:
        app_engine = AppDependencyCollection(session)
        yield app_engine
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# Specifies our desired OAuth2 access scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


# Dependency class for an OAuth2-compatible access token, to be
# used for endpoints requiring authorization. Its inclusion in
# the parameters of an endpoint handler will require a valid 
# 'authorization' header
AccessTokenDependency = Annotated[str, Depends(oauth2_scheme)]

def get_user_from_token(
    app_engine: Annotated[AppDependencyCollection, Depends(get_engine)],
    token: AccessTokenDependency
) -> User:
    '''
    Retrieves the user associated with the specified token
    '''

    # Grab the access token specified
    access_token = app_engine.token_repository.get_token_by_id(token)

    # Abort if the access token cannot be found or is revoked
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="forbidden"
        )

    # Abort if the token has expired
    if access_token.expires_at < get_current_time():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="expired"
        )

    # If execution reaches here, we can use the token. Grab the user
    # account associated with this token
    user = app_engine.user_repository.get_user_by_id(access_token.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid token"
        )

    return user


# Dependency class for the current authenticated user, to be used for
# endpoints requring the user requesting the operation.
CurrentUserDependency = Annotated[User, Depends(get_user_from_token)]

