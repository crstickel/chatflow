
from email_validator import validate_email, EmailNotValidError

from app.dependencies import engine, AppDependencyCollection
from app.models.user import User

from shared.password import hash_password

class AuthService:

    def __init__(self, engine: AppDependencyCollection):
        self.engine = engine


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

