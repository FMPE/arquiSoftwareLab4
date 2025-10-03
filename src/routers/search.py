from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.schemas import SearchQuery, SearchResponse, Message
from ..services import search_papers_service, search_authors_service, get_search_suggestions

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.get("/papers", response_model=SearchResponse, summary="Buscar papers")
async def search_papers_endpoint(
    q: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Buscar papers por título o contenido.
    
    - **q**: Término de búsqueda (requerido)
    - **limit**: Número máximo de resultados (default: 10)
    - **offset**: Número de resultados a omitir para paginación (default: 0)
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    search_query = SearchQuery(q=q.strip(), limit=limit, offset=offset)
    return search_papers_service(db, search_query)

@router.get("/authors", response_model=SearchResponse, summary="Buscar por autor")
async def search_authors_endpoint(
    q: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Buscar papers por nombre de autor.
    
    - **q**: Nombre del autor a buscar (requerido)
    - **limit**: Número máximo de resultados (default: 10)
    - **offset**: Número de resultados a omitir para paginación (default: 0)
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre del autor debe tener al menos 2 caracteres"
        )
    
    search_query = SearchQuery(q=q.strip(), limit=limit, offset=offset)
    return search_authors_service(db, search_query)

@router.get("/suggestions", response_model=List[str], summary="Obtener sugerencias de búsqueda")
async def get_suggestions_endpoint(q: str):
    """
    Obtener sugerencias de términos de búsqueda.
    
    - **q**: Término parcial para generar sugerencias
    """
    if not q or len(q.strip()) < 1:
        return []
    
    suggestions = get_search_suggestions(q.strip())
    return suggestions
