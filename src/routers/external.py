from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models.schemas import ExternalSearchResponse
from ..services import external_api_mock
from ..config import settings

router = APIRouter(prefix="/api/v1/external", tags=["external-repositories"])

@router.get("/papers", response_model=List[ExternalSearchResponse], summary="Buscar en repositorios externos")
async def search_external_repositories(
    q: str = "machine learning",
    limit_per_source: int = 3
):
    """
    Buscar papers en repositorios académicos externos simulados.
    
    - **q**: Término de búsqueda (default: "machine learning")
    - **limit_per_source**: Límite de resultados por fuente (default: 3)
    
    Fuentes simuladas:
    - arXiv
    - IEEE Xplore
    - ACM Digital Library
    """
    if not settings.mock_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mock de APIs externas está deshabilitado"
        )
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    try:
        results = external_api_mock.search_all_sources(q.strip(), limit_per_source)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar repositorios externos: {str(e)}"
        )

@router.get("/arxiv", response_model=ExternalSearchResponse, summary="Buscar en arXiv")
async def search_arxiv(
    q: str = "deep learning",
    limit: int = 5
):
    """
    Buscar papers específicamente en arXiv (simulado).
    
    - **q**: Término de búsqueda
    - **limit**: Número máximo de resultados
    """
    if not settings.mock_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mock de APIs externas está deshabilitado"
        )
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    try:
        result = external_api_mock.search_arxiv(q.strip(), limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar arXiv: {str(e)}"
        )

@router.get("/ieee", response_model=ExternalSearchResponse, summary="Buscar en IEEE Xplore")
async def search_ieee(
    q: str = "computer vision",
    limit: int = 5
):
    """
    Buscar papers específicamente en IEEE Xplore (simulado).
    
    - **q**: Término de búsqueda
    - **limit**: Número máximo de resultados
    """
    if not settings.mock_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mock de APIs externas está deshabilitado"
        )
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    try:
        result = external_api_mock.search_ieee(q.strip(), limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar IEEE Xplore: {str(e)}"
        )

@router.get("/acm", response_model=ExternalSearchResponse, summary="Buscar en ACM Digital Library")
async def search_acm(
    q: str = "software engineering",
    limit: int = 5
):
    """
    Buscar papers específicamente en ACM Digital Library (simulado).
    
    - **q**: Término de búsqueda
    - **limit**: Número máximo de resultados
    """
    if not settings.mock_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mock de APIs externas está deshabilitado"
        )
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    
    try:
        result = external_api_mock.search_acm(q.strip(), limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar ACM Digital Library: {str(e)}"
        )
