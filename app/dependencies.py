
from functools import cached_property

from app.repositories.user import UserRespository, InMemoryUserRepository


class AppDependencyCollection:

    @cached_property
    def user_repository(self) -> UserRespository:
        return InMemoryUserRepository()


engine = AppDependencyCollection()

