from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .models import Base
from ..config import settings
import os

# Crear el directorio data si no existe
os.makedirs("data", exist_ok=True)

# Crear engine de base de datos
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# Crear session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)
def get_db() -> Generator[Session, None, None]:
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear las tablas al importar el módulo
create_tables()

# Crear las tablas al importar el módulo
create_tables()
