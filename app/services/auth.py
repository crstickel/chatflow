
from email_validator import validate_email, EmailNotValidError
from typing import Optional

from app.dependencies import AppDependencyCollection
from app.models.accesstoken import AccessToken
from app.models.user import User

from shared.password import hash_password, verify_password

class AuthService:

    def __init__(self, engine: AppDependencyCollection):
        self.engine = engine


    def login_user(self, username: str, password: str) -> Optional[AccessToken]:
        '''
        Implements OAuth2's "resource-owner password grant" flow, allowing a user to provide their
        username and password in order to retrieve an access & refresh token pair.

        Returns an access token that the user shall use to authenticate their requests. If the
        operation fails, it returns None. No further information shall be provided.
        '''

        # Retrieve the user account specified
        user = self.engine.user_repository.get_user_by_username(username)
        if user is None:
            return None

        # Verify the provided password
        if not verify_password(password, user.pwhash):
            return None

        # If execution reaches here, the user has been authenticated! We can issue tokens
        token = self.engine.token_repository.create_token(user.id)
        return token


    def register_new_user(self, username: str, email: str, password: str) -> User:
        '''
        Creates a new user account
        '''

        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise ValueError(f"'{email}' is not a valid email address: {str(e.args[0])}")

        # TODO : check for duplicate user names

        user = engine.user_repository.create_user(
            id=User.generate_id(),
            username=username,
            email=email,
            pwhash=hash_password(password)
        )

        return user

