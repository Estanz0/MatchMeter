from sqlalchemy.orm import Session
from . import models, schemas
from .services.openai import MatchResult

def get_comparison(db: Session, comparison_id: int):
    return db.query(models.Comparison).filter(models.Comparison.id == comparison_id).first()

def get_comparisons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Comparison).offset(skip).limit(limit).all()

def create_comparison(db: Session, comparison: schemas.ComparisonCreate, match_result: MatchResult):
    db_comparison = models.Comparison(**comparison.model_dump(), **match_result.model_dump())
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    return db_comparison
