
from functools import cached_property
from typing import Self

from app.repositories.user import UserRepository, InMemoryUserRepository


class AppDependencyCollection:

    @cached_property
    def user_repository(self) -> UserRepository:
        return InMemoryUserRepository()


    def __call__(self) -> Self:
        '''
        Dunder/magic method which allows the instance itself to be called, which provides
        compatibility with FastAPI's dependency injection system via Depends(..)
        '''

        return self


engine = AppDependencyCollection()

