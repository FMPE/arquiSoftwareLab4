from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Schemas para User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Schemas para Paper
class PaperBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    authors: Optional[List[str]] = []
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    keywords: Optional[List[str]] = []

class PaperCreate(PaperBase):
    pass

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    abstract: Optional[str] = None
    authors: Optional[List[str]] = None
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    keywords: Optional[List[str]] = None

class Paper(PaperBase):
    id: int
    citation_count: int
    created_at: datetime
    updated_at: datetime
    creator_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Schemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schemas para búsqueda
class SearchQuery(BaseModel):
    q: str
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[Paper]
    
# Schema para mock external API
class ExternalPaper(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: Optional[str] = None
    source: str  # "arxiv", "ieee", etc.
    url: Optional[str] = None

class ExternalSearchResponse(BaseModel):
    query: str
    source: str
    total: int
    papers: List[ExternalPaper]

# Schemas para respuestas generales
class Message(BaseModel):
    message: str

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
