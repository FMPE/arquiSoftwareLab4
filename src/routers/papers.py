from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.schemas import Paper, PaperCreate, PaperUpdate, Message
from ..services import (
    get_papers, get_paper_by_id, create_paper, update_paper, delete_paper,
    get_popular_papers, convert_db_paper_to_schema, verify_token, get_user_by_username
)

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Dependency para obtener ID del usuario actual (opcional)"""
    try:
        username = verify_token(credentials.credentials)
        if username:
            user = get_user_by_username(db, username)
            return user.id if user else None
    except:
        pass
    return None

@router.get("/", response_model=List[Paper], summary="Obtener lista de papers")
async def list_papers(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    Obtener lista paginada de papers.
    
    - **skip**: Número de papers a omitir (para paginación)
    - **limit**: Número máximo de papers a retornar
    """
    db_papers = get_papers(db, skip=skip, limit=limit)
    papers = []
    for db_paper in db_papers:
        paper_dict = convert_db_paper_to_schema(db_paper)
        papers.append(Paper(**paper_dict))
    return papers

@router.get("/popular", response_model=List[Paper], summary="Obtener papers populares")
async def list_popular_papers(
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    Obtener papers más populares ordenados por citation_count.
    
    - **limit**: Número máximo de papers a retornar
    """
    db_papers = get_popular_papers(db, limit=limit)
    papers = []
    for db_paper in db_papers:
        paper_dict = convert_db_paper_to_schema(db_paper)
        papers.append(Paper(**paper_dict))
    return papers

@router.get("/{paper_id}", response_model=Paper, summary="Obtener paper específico")
async def get_paper(paper_id: int, db: Session = Depends(get_db)):
    """
    Obtener un paper específico por su ID.
    
    - **paper_id**: ID único del paper
    """
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper no encontrado"
        )
    
    paper_dict = convert_db_paper_to_schema(db_paper)
    return Paper(**paper_dict)

@router.post("/", response_model=Paper, status_code=status.HTTP_201_CREATED, summary="Crear nuevo paper")
async def create_new_paper(
    paper_data: PaperCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Crear un nuevo paper en el sistema.
    
    - **title**: Título del paper (requerido)
    - **abstract**: Resumen del paper
    - **authors**: Lista de autores
    - **publication_year**: Año de publicación
    - **doi**: Identificador DOI
    - **pdf_url**: URL del archivo PDF
    - **keywords**: Lista de palabras clave
    """
    # Verificar si ya existe un paper con el mismo DOI
    if paper_data.doi:
        from ..services import get_paper_by_doi
        existing_paper = get_paper_by_doi(db, paper_data.doi)
        if existing_paper:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un paper con este DOI"
            )
    
    db_paper = create_paper(db, paper_data, current_user_id)
    paper_dict = convert_db_paper_to_schema(db_paper)
    return Paper(**paper_dict)

@router.put("/{paper_id}", response_model=Paper, summary="Actualizar paper")
async def update_existing_paper(
    paper_id: int, 
    paper_update: PaperUpdate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Actualizar un paper existente.
    
    - **paper_id**: ID del paper a actualizar
    - Solo se actualizarán los campos proporcionados
    """
    # Verificar que el paper existe
    existing_paper = get_paper_by_id(db, paper_id)
    if not existing_paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper no encontrado"
        )
    
    # Verificar autorización (opcional: solo el creador puede editar)
    if current_user_id and existing_paper.creator_id and existing_paper.creator_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este paper"
        )
    
    updated_paper = update_paper(db, paper_id, paper_update)
    if not updated_paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper no encontrado"
        )
    
    paper_dict = convert_db_paper_to_schema(updated_paper)
    return Paper(**paper_dict)

@router.delete("/{paper_id}", response_model=Message, summary="Eliminar paper")
async def delete_existing_paper(
    paper_id: int, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Eliminar un paper del sistema.
    
    - **paper_id**: ID del paper a eliminar
    """
    # Verificar que el paper existe
    existing_paper = get_paper_by_id(db, paper_id)
    if not existing_paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper no encontrado"
        )
    
    # Verificar autorización (opcional: solo el creador puede eliminar)
    if current_user_id and existing_paper.creator_id and existing_paper.creator_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este paper"
        )
    
    success = delete_paper(db, paper_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper no encontrado"
        )
    
    return Message(message="Paper eliminado exitosamente")
