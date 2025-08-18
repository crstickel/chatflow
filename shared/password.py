
import argon2


# Limit exported symbols to just routines
__all__ = [ "hash_password", "verify_password", "is_needing_rehash" ]


# Argon2 profile for the password hasher. The following settings define the
# operational requirements for the hasher. Changing these will either
# hinder the performance of the service or the security of our password
# storage.
_hasher = argon2.PasswordHasher(
    time_cost = 3,
    memory_cost = 65536,
    parallelism = 4,
    hash_len = 32,
    salt_len = 16
)


def hash_password(plaintext: str) -> str:
    '''
    Hashes the specified plaintext into a password hash safe for storage.
    '''
    return _hasher.hash(plaintext.encode(encoding='utf-8', errors='strict'))


def verify_password(plaintext: str, hashed: str) -> bool:
    '''
    Returns True when the specified plaintext corresponds to the hashed value,
    and False if it does not. Any exceptions incurred during execution are
    escalted as they indicate a potential data-handing issue.
    '''
    try:
        _hasher.verify(hashed, plaintext)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
    except argon2.exceptions.VerificationError:
        raise
    except argon2.exceptions.InvalidHashError:
        raise


def is_needing_rehash(hashed: bytes) -> bool:
    '''
    Checks the metadata of the hash and determines if it meets our current configured standards.
    If result is False, then the password should be rehashed and the best time to do so is after
    a successful login where we know the plaintext is correct.
    '''
    return _hasher.check_needs_rehash(hashed)

