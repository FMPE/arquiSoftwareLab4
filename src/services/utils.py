from sqlalchemy.orm import Session
from ..database.models import Paper as DBPaper
from ..models.schemas import PaperCreate, PaperUpdate
from typing import Optional

def get_paper_by_doi(db: Session, doi: str) -> Optional[DBPaper]:
    """Obtener paper por DOI (función faltante)"""
    return db.query(DBPaper).filter(DBPaper.doi == doi).first()
