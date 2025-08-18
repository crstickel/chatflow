
from abc import ABC, abstractmethod
from typing import Optional, List

from app.models.user import User
from shared.time import get_current_time


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, id: str, username: str, email: str, pwhash: str):
        '''
        Creates and adds a new User model instance to the repository
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_num_users(self) -> int:
        '''
        Returns the number of users currently being stored in this repository
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_user_by_id(self, id: str) -> Optional[User]:
        '''
        Retrieves a user account based on the specified ID
        '''
        raise NotImplementedError()


    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        '''
        Retrieves a user account based on the specified email address
        '''
        raise NotImplementedError()


    @abstractmethod
    def update_user(self, id: str, user: User) -> None:
        '''
        Updates a user's data in the repository.
        Raises:
        - KeyError if the user cannot be found
        - ValueError if the 'id' field changes
        '''
        raise NotImplementedError()


    @abstractmethod
    def delete_user_by_id(self, id: str) -> None:
        '''
        Deletes a user
        Raises: KeyError if the user cannot be found
        '''
        raise NotImplementedError()



class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users_by_id = {}
        self.ids_by_email = {}


    def create_user(self, username: str, email: str, pwhash: str):
        '''
        Creates and adds a new User model instance to the repository
        Raises a ValueError exception upon ID collision
        '''

        user = User(
            id=User.generate_id(),
            username=username,
            email=email,
            pwhash=pwhash,
            created_at=get_current_time(),
            deleted_at=None
        )

        if user.id in self.users_by_id:
            raise ValueError(f"User with id={user.id} already exists in repository")

        self.users_by_id[user.id] = user
        self.ids_by_email[user.email] = user.id

        return user


    def get_num_users(self) -> int:
        '''
        Returns the number of users currently being stored in this repository
        '''
        return len(self.users_by_id)


    def get_user_by_id(self, id: str) -> Optional[User]:
        '''
        Retrieves a user account based on the specified ID
        '''
        user = self.users_by_id.get(id, None)
        if user is None:
            return None
        return user.model_copy()


    def get_user_by_email(self, email: str) -> Optional[User]:
        '''
        Retrieves a user account based on the specified email address
        '''
        id = self.ids_by_email.get(email, None)
        if id is None:
            return None
        return self.get_user_by_id(id)


    def update_user(self, id: str, user: User) -> None:
        '''
        Updates a user's data in the repository.
        Raises:
        - KeyError if the user cannot be found
        - ValueError if the 'id' field changes
        '''

        record = self.get_user_by_id(id)
        if record is None:
            raise KeyError(f"User with id '{id}' cannot be found")
        if record.id != user.id:
            raise ValueError('Cannot change id')

        self.users_by_id[record.id] = user

        # Special case: we need to re-index if the email address changed
        if record.email != user.email:
            del self.ids_by_email[record.email]
            self.ids_by_email[user.email] = record.id


    def delete_user_by_id(self, id: str) -> None:
        '''
        Deletes a user
        Raises: KeyError if the user cannot be found
        '''
        user = self.get_user_by_id(id)
        if user is None:
            raise KeyError(f"User with id '{id}' cannot be found")

        user.deleted_at = get_current_time()
        self.update_user(id, user)


