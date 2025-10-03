from sqlalchemy.orm import Session
from ..database.models import User as DBUser
from ..models.schemas import UserCreate, UserLogin
from .auth_service import get_password_hash, verify_password
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[DBUser]:
    """Obtener usuario por username"""
    return db.query(DBUser).filter(DBUser.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[DBUser]:
    """Obtener usuario por email"""
    return db.query(DBUser).filter(DBUser.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[DBUser]:
    """Obtener usuario por ID"""
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> DBUser:
    """Crear nuevo usuario"""
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[DBUser]:
    """Autenticar usuario"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_activity(db: Session, user_id: int):
    """Actualizar última actividad del usuario (opcional)"""
    pass  # Implementar si se necesita tracking de actividad
