
from functools import cached_property

from app.repositories.user import UserRepository, InMemoryUserRepository


class AppDependencyCollection:

    @cached_property
    def user_repository(self) -> UserRepository:
        return InMemoryUserRepository()


engine = AppDependencyCollection()

