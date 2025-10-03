from sqlalchemy.orm import Session
from ..database.models import Paper as DBPaper, SearchLog
from ..models.schemas import PaperCreate, PaperUpdate, SearchQuery
from typing import List, Optional
import json

def get_paper_by_doi(db: Session, doi: str) -> Optional[DBPaper]:
    """Obtener paper por DOI"""
    return db.query(DBPaper).filter(DBPaper.doi == doi).first()

def get_papers(db: Session, skip: int = 0, limit: int = 100) -> List[DBPaper]:
    """Obtener lista de papers"""
    return db.query(DBPaper).offset(skip).limit(limit).all()

def get_paper_by_id(db: Session, paper_id: int) -> Optional[DBPaper]:
    """Obtener paper por ID"""
    return db.query(DBPaper).filter(DBPaper.id == paper_id).first()

def get_paper_by_doi(db: Session, doi: str) -> Optional[DBPaper]:
    """Obtener paper por DOI"""
    return db.query(DBPaper).filter(DBPaper.doi == doi).first()

def create_paper(db: Session, paper: PaperCreate, creator_id: Optional[int] = None) -> DBPaper:
    """Crear nuevo paper"""
    # Convertir listas a JSON strings
    authors_json = json.dumps(paper.authors) if paper.authors else "[]"
    keywords_json = json.dumps(paper.keywords) if paper.keywords else "[]"
    
    db_paper = DBPaper(
        title=paper.title,
        abstract=paper.abstract,
        authors=authors_json,
        publication_year=paper.publication_year,
        doi=paper.doi,
        pdf_url=paper.pdf_url,
        keywords=keywords_json,
        creator_id=creator_id
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def update_paper(db: Session, paper_id: int, paper_update: PaperUpdate) -> Optional[DBPaper]:
    """Actualizar paper existente"""
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        return None
    
    update_data = paper_update.dict(exclude_unset=True)
    
    # Convertir listas a JSON si están presentes
    if 'authors' in update_data and update_data['authors'] is not None:
        update_data['authors'] = json.dumps(update_data['authors'])
    if 'keywords' in update_data and update_data['keywords'] is not None:
        update_data['keywords'] = json.dumps(update_data['keywords'])
    
    for field, value in update_data.items():
        setattr(db_paper, field, value)
    
    db.commit()
    db.refresh(db_paper)
    return db_paper

def delete_paper(db: Session, paper_id: int) -> bool:
    """Eliminar paper"""
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        return False
    
    db.delete(db_paper)
    db.commit()
    return True

def search_papers(db: Session, query: str, skip: int = 0, limit: int = 10) -> List[DBPaper]:
    """Buscar papers por título o contenido"""
    return db.query(DBPaper).filter(
        DBPaper.title.contains(query)
    ).offset(skip).limit(limit).all()

def search_papers_by_author(db: Session, author_query: str, skip: int = 0, limit: int = 10) -> List[DBPaper]:
    """Buscar papers por autor"""
    return db.query(DBPaper).filter(
        DBPaper.authors.contains(author_query)
    ).offset(skip).limit(limit).all()

def log_search(db: Session, query: str, results_count: int, search_type: str = "papers", user_id: Optional[int] = None):
    """Registrar búsqueda en logs"""
    search_log = SearchLog(
        query=query,
        user_id=user_id,
        results_count=results_count,
        search_type=search_type
    )
    db.add(search_log)
    db.commit()

def get_popular_papers(db: Session, limit: int = 10) -> List[DBPaper]:
    """Obtener papers más populares por citation_count"""
    return db.query(DBPaper).order_by(DBPaper.citation_count.desc()).limit(limit).all()

def convert_db_paper_to_schema(db_paper: DBPaper):
    """Convertir DBPaper a schema Paper con parsing de JSON"""
    authors = json.loads(db_paper.authors) if db_paper.authors else []
    keywords = json.loads(db_paper.keywords) if db_paper.keywords else []
    
    return {
        "id": db_paper.id,
        "title": db_paper.title,
        "abstract": db_paper.abstract,
        "authors": authors,
        "publication_year": db_paper.publication_year,
        "doi": db_paper.doi,
        "pdf_url": db_paper.pdf_url,
        "keywords": keywords,
        "citation_count": db_paper.citation_count,
        "created_at": db_paper.created_at,
        "updated_at": db_paper.updated_at,
        "creator_id": db_paper.creator_id
    }
