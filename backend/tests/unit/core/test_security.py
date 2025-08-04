import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    ALGORITHM
)

# --- Test Password Hashing ---

def test_get_password_hash():
    """Test that a password gets hashed correctly."""
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert isinstance(hashed_password, str)

def test_verify_password():
    """Test that a correct plain password is verified against its hash."""
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True

def test_verify_password_incorrect():
    """Test that an incorrect plain password is not verified."""
    password = "mysecretpassword"
    wrong_password = "wrongsecret"
    hashed_password = get_password_hash(password)
    assert verify_password(wrong_password, hashed_password) is False

# --- Test JWT Creation and Decoding ---

def test_create_access_token():
    """Test that an access token is created with the correct subject and expiry."""
    subject = "testuser@example.com"
    token = create_access_token(subject)
    
    payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
    
    assert payload["sub"] == subject
    
    # Check that the token expires in the future, within the configured time
    expire_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected_expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    assert expire_time > datetime.now(timezone.utc)
    # Allow a small tolerance for the time difference during execution
    assert (expected_expire_time - expire_time).total_seconds() < 5

def test_create_access_token_with_custom_expiry():
    """Test that an access token can be created with a custom expiry delta."""
    subject = "testuser_custom_expiry"
    delta = timedelta(minutes=10)
    token = create_access_token(subject, expires_delta=delta)
    
    payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
    
    expire_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected_expire_time = datetime.now(timezone.utc) + delta
    
    assert (expected_expire_time - expire_time).total_seconds() < 5

def test_create_access_token_with_additional_claims():
    """Test that additional claims can be added to the token payload."""
    subject = "testuser_claims"
    claims = {"organization_id": "org_123", "role": "admin"}
    token = create_access_token(subject, additional_claims=claims)
    
    payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
    
    assert payload["sub"] == subject
    assert payload["organization_id"] == "org_123"
    assert payload["role"] == "admin"

def test_decode_token_valid():
    """Test that a valid token is decoded correctly."""
    subject = "testuser_valid_decode"
    token = create_access_token(subject)
    
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == subject

def test_decode_token_expired(monkeypatch):
    """Test that an expired token returns None."""
    subject = "testuser_expired"
    # Create a token that expired 1 minute ago
    expired_delta = timedelta(minutes=-1)
    token = create_access_token(subject, expires_delta=expired_delta)
    
    payload = decode_token(token)
    assert payload is None

def test_decode_token_invalid_signature():
    """Test that a token with an invalid signature returns None."""
    subject = "testuser_invalid_sig"
    token = create_access_token(subject)
    
    # Tamper with the token
    tampered_token = token + "tamper"
    
    payload = decode_token(tampered_token)
    assert payload is None

def test_decode_token_invalid_algorithm():
    """Test that a token with a different algorithm is rejected."""
    subject = "testuser_wrong_algo"
    to_encode = {"sub": subject, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
    # Encode with a different algorithm
    wrong_algo_token = jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(), algorithm="HS512")
    
    payload = decode_token(wrong_algo_token)
    assert payload is None
