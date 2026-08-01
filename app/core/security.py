# app/core/security.py

from pwdlib import PasswordHash

# Create a single reusable password hasher instance.
_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.

    Args:
        password: The user's plain-text password.

    Returns:
        The hashed password.
    """
    return _password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored hash.

    Args:
        password: The plain-text password.
        hashed_password: The stored password hash.

    Returns:
        True if the password is correct, otherwise False.
    """
    return _password_hash.verify(password, hashed_password)


def password_needs_rehash(hashed_password: str) -> bool:
    """
    Check whether a stored password hash should be upgraded.

    This is useful when the hashing algorithm or its parameters
    have changed since the password was originally hashed.

    Args:
        hashed_password: The stored password hash.

    Returns:
        True if the password should be rehashed.
    """
    return _password_hash.needs_rehash(hashed_password)