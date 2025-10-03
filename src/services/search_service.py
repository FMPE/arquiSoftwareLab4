from sqlalchemy.orm import Session
from .paper_service import search_papers, search_papers_by_author, log_search, convert_db_paper_to_schema
from ..models.schemas import SearchQuery, SearchResponse, Paper
from typing import List, Optional

# Cache simple en memoria para resultados de búsqueda
search_cache = {}

def search_papers_service(db: Session, search_query: SearchQuery, user_id: Optional[int] = None) -> SearchResponse:
    """Servicio principal de búsqueda de papers"""
    
    # Verificar cache simple
    cache_key = f"papers_{search_query.q}_{search_query.offset}_{search_query.limit}"
    if cache_key in search_cache:
        cached_result = search_cache[cache_key]
        # Log de búsqueda
        log_search(db, search_query.q, len(cached_result["results"]), "papers", user_id)
        return SearchResponse(**cached_result)
    
    # Buscar en base de datos
    db_papers = search_papers(
        db, 
        search_query.q, 
        search_query.offset, 
        search_query.limit
    )
    
    # Convertir a schemas
    papers = []
    for db_paper in db_papers:
        paper_dict = convert_db_paper_to_schema(db_paper)
        papers.append(Paper(**paper_dict))
    
    # Crear respuesta
    response_data = {
        "query": search_query.q,
        "total": len(papers),
        "results": papers
    }
    
    # Guardar en cache
    search_cache[cache_key] = response_data
    
    # Log de búsqueda
    log_search(db, search_query.q, len(papers), "papers", user_id)
    
    return SearchResponse(**response_data)

def search_authors_service(db: Session, search_query: SearchQuery, user_id: Optional[int] = None) -> SearchResponse:
    """Servicio de búsqueda por autores"""
    
    # Verificar cache
    cache_key = f"authors_{search_query.q}_{search_query.offset}_{search_query.limit}"
    if cache_key in search_cache:
        cached_result = search_cache[cache_key]
        log_search(db, search_query.q, len(cached_result["results"]), "authors", user_id)
        return SearchResponse(**cached_result)
    
    # Buscar por autor
    db_papers = search_papers_by_author(
        db, 
        search_query.q, 
        search_query.offset, 
        search_query.limit
    )
    
    # Convertir a schemas
    papers = []
    for db_paper in db_papers:
        paper_dict = convert_db_paper_to_schema(db_paper)
        papers.append(Paper(**paper_dict))
    
    response_data = {
        "query": search_query.q,
        "total": len(papers),
        "results": papers
    }
    
    # Guardar en cache
    search_cache[cache_key] = response_data
    
    # Log de búsqueda
    log_search(db, search_query.q, len(papers), "authors", user_id)
    
    return SearchResponse(**response_data)

def get_search_suggestions(query: str) -> List[str]:
    """Obtener sugerencias de búsqueda simples"""
    # Implementación básica de sugerencias
    common_terms = [
        "machine learning", "artificial intelligence", "deep learning",
        "computer vision", "natural language processing", "data science",
        "algorithms", "software engineering", "cybersecurity", "blockchain"
    ]
    
    suggestions = [term for term in common_terms if query.lower() in term.lower()]
    return suggestions[:5]  # Máximo 5 sugerencias

def clear_search_cache():
    """Limpiar cache de búsquedas"""
    global search_cache
    search_cache.clear()
