# app/core/security.py

from pwdlib import PasswordHash 
import jwt

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

def create_jwt_token(payload: dict, public_key: str="secret",algorithm: str="HS256" ):
    """ 
    create jwt token.
    returns:
        JWT Token
    Parameters:
        payload: 
            The payload must store in  JWT Token.
        key:
            Secret_key. (better to load from environment variable)
        algorithm:
            algorithm of encoding.
    """
    import dotenv ,os, datetime
    from datetime import timedelta , timezone
    
    dotenv.load_dotenv()
    
    expires_delta= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(payload=to_encode, key=public_key, algorithm=algorithm)

def decode_jwt_token(JWT_Token_encoded: str, public_key: str="secret",algorithm: str="HS256" ):
    """ 
    encoded jwt token.
    returns:
        Payload stored in JWT Token.
    Parameters:
        payload: 
            encoded JWT Token.
        key:
            Secret_key. (better to load from environment variable)
        algorithm:
            algorithm of encoding/decoding.
    """
    return jwt.decode(JWT_Token_encoded, public_key, algorithms=[algorithm])