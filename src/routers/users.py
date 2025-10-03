from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models.schemas import User, UserCreate, UserLogin, Token, Message
from ..services import (
    get_user_by_username, get_user_by_email, create_user, authenticate_user,
    create_access_token, verify_token
)
from ..config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency para obtener el usuario actual autenticado"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo usuario")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario en el sistema.
    
    - **username**: Nombre de usuario único (requerido)
    - **email**: Correo electrónico único (requerido)
    - **password**: Contraseña (requerido)
    - **full_name**: Nombre completo (opcional)
    """
    # Verificar si el usuario ya existe
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    # Verificar si el email ya existe
    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Crear el usuario
    db_user = create_user(db, user_data)
    return User.from_orm(db_user)

@router.post("/login", response_model=Token, summary="Iniciar sesión")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token de acceso.
    
    - **username**: Nombre de usuario
    - **password**: Contraseña
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login-json", response_model=Token, summary="Iniciar sesión (JSON)")
async def login_user_json(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión con datos JSON y obtener token de acceso.
    
    - **username**: Nombre de usuario
    - **password**: Contraseña
    """
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile", response_model=User, summary="Obtener perfil del usuario")
async def get_user_profile(current_user = Depends(get_current_user)):
    """
    Obtener el perfil del usuario autenticado.
    
    Requiere token de autenticación válido.
    """
    return User.from_orm(current_user)

@router.get("/verify", response_model=Message, summary="Verificar token")
async def verify_token_endpoint(current_user = Depends(get_current_user)):
    """
    Verificar si el token actual es válido.
    
    Requiere token de autenticación válido.
    """
    return Message(message=f"Token válido para usuario: {current_user.username}")
