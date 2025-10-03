import hashlib
import hmac
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from ..config import settings

def simple_hash_password(password: str) -> str:
    """Hash simple y seguro de contraseña usando SHA-256 + salt"""
    # Usar el secret key como salt
    salt = settings.jwt_secret_key.encode()
    password_bytes = password.encode('utf-8')
    
    # Crear hash con salt
    hash_obj = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    return hash_obj.hex()

def verify_simple_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña con hash simple"""
    try:
        return simple_hash_password(plain_password) == hashed_password
    except Exception:
        return False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar password con fallback a método simple"""
    try:
        # Intentar primero con passlib/bcrypt
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback a método simple
        return verify_simple_password(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generar hash de password con fallback"""
    try:
        # Intentar primero con passlib/bcrypt
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Truncar contraseña si es muy larga para bcrypt
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        
        return pwd_context.hash(password)
    except Exception as e:
        print(f"bcrypt no disponible, usando hash simple: {e}")
        # Fallback a método simple pero seguro
        return simple_hash_password(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
