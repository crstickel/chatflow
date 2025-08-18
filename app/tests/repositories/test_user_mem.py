
import pytest
import uuid

from app.models.user import User
from app.repositories.user import UserRepository, InMemoryUserRepository

###################################################################################################
#
#   Fixtures
#
###################################################################################################


@pytest.fixture(scope='module')
def test_user_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope='module')
def test_user_name() -> str:
    return "testaccount"


@pytest.fixture(scope='module')
def test_user_email() -> str:
    return "test@example.com"


@pytest.fixture(scope='function')
def empty_repository() -> UserRepository:
    return InMemoryUserRepository()


@pytest.fixture(scope='function')
def populated_repository(
    test_user_id: str,
    test_user_name: str,
    test_user_email: str
) -> UserRepository:
    repo = InMemoryUserRepository()
    repo.create_user(
        id=test_user_id,
        username=test_user_name,
        email=test_user_email,
        pwhash='dummypwhash'
    )
    return repo



###################################################################################################
#
#   Tests
#
###################################################################################################

def test_create_user(empty_repository: UserRepository):
    assert empty_repository.get_num_users() == 0
    user = empty_repository.create_user(
        username='test',
        email='test@example.com',
        pwhash='dummydatafornow'
    )

    assert user.id != None
    assert user.id != ''
    assert empty_repository.get_num_users() == 1
    assert empty_repository.users_by_id[user.id].email == 'test@example.com'



def test_get_user_by_id(populated_repository: UserRepository, test_user_id: str):
    retrieved = populated_repository.get_user_by_id(test_user_id)
    assert retrieved is not None
    assert retrieved.id == test_user_id


def test_get_user_by_bad_id(populated_repository: UserRepository, test_user_id: str):
    retrieved = populated_repository.get_user_by_id('thisisnotanid')
    assert retrieved is None


def test_get_user_by_email(populated_repository: UserRepository, test_user_email: str):
    retrieved = populated_repository.get_user_by_email(test_user_email)
    assert retrieved is not None
    assert retrieved.email == test_user_email


def test_get_user_by_bad_email(populated_repository: UserRepository, test_user_email: str):
    retrieved = populated_repository.get_user_by_email('wrong@example.com')
    assert retrieved is None


def test_get_user_by_username(populated_repository: UserRepository, test_user_name: str):
    retrieved = populated_repository.get_user_by_username(test_user_name)
    assert retrieved is not None
    assert retrieved.username == test_user_name


def test_get_user_by_bad_username(populated_repository: UserRepository, test_user_name: str):
    retrieved = populated_repository.get_user_by_username('leeeeeeroyhhhhhnnnnjennnnnkins')
    assert retrieved is None


def test_update_user(populated_repository: UserRepository, test_user_id: str):
    user = populated_repository.get_user_by_id(test_user_id)
    user.pwhash = 'yetanotherhash'

    populated_repository.update_user(test_user_id, user)

    retrieved = populated_repository.get_user_by_id(test_user_id)
    assert retrieved is not None
    assert retrieved.pwhash == 'yetanotherhash'


def test_delete_user_by_id(populated_repository: UserRepository, test_user_id: str):
    populated_repository.delete_user_by_id(test_user_id)
    retrieved = populated_repository.get_user_by_id(test_user_id)
    assert retrieved is None

