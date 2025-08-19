
from abc import ABC, abstractmethod
from sqlmodel import Session
from typing import Optional, List

from app.models.accesstoken import AccessToken
from shared.time import get_current_time


class AccessTokenRepository(ABC):

    @abstractmethod
    def create_token(self, user_id: str) -> AccessToken:
        '''
        Creates and adds a new User model instance to the repository
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_token_by_id(self, id: str) -> Optional[AccessToken]:
        '''
        Retrieves an access token based on the specified ID
        '''
        raise NotImplementedError()


    @abstractmethod
    def delete_token_by_id(self, id: str) -> None:
        '''
        Deletes an access token
        Raises: KeyError if the user cannot be found
        '''
        raise NotImplementedError()



class InMemoryAccessTokenRepository(AccessTokenRepository):

    def __init__(self):
        self.tokens = {}


    def create_token(self, user_id: str) -> AccessToken:
        '''
        Creates and adds a new AccessToken instance to the repository
        '''

        token = AccessToken(
            id=AccessToken.generate_id(),
            user_id=user_id,
            created_at=get_current_time(),
            time_to_live=AccessToken.default_time_to_live()
        )

        self.tokens[token.id] = token
        return token


    def get_token_by_id(self, id: str) -> Optional[AccessToken]:
        '''
        Retrieves an access token based on the specified ID
        '''
        token = self.tokens.get(id, None)
        if token is None:
            return None

        return token.model_copy()


    def delete_token_by_id(self, id: str) -> None:
        '''
        Deletes an access token
        Raises: KeyError if the user cannot be found
        '''
        del self.tokens[id]


class DbAccessTokenRepository(AccessTokenRepository):

    def __init__(self, session: Session):
        self.session = session


    def create_token(self, user_id: str) -> AccessToken:
        '''
        Creates and adds a new AccessToken instance to the repository
        '''

        token = AccessToken(
            id=AccessToken.generate_id(),
            user_id=user_id,
            created_at=get_current_time(),
            time_to_live=AccessToken.default_time_to_live()
        )
        self.session.add(token)
        self.session.commit()
        return token


    def get_token_by_id(self, id: str) -> Optional[AccessToken]:
        '''
        Retrieves an access token based on the specified ID
        '''
        return self.session.get(AccessToken, id)


    def delete_token_by_id(self, id: str) -> None:
        '''
        Deletes an access token
        '''
        token = self.session.get_user_by_id(id)
        self.session.delete(token)
        self.session.commit()

