from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from .services.openai import calculate_match_score

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/comparisons/", response_model=schemas.Comparison)
def create_comparison(comparison: schemas.ComparisonCreate, db: Session = Depends(get_db)):
    match_result = calculate_match_score(comparison.input1, comparison.input2)  # Implement this function
    return crud.create_comparison(db=db, comparison=comparison, match_result=match_result)

@app.get("/comparisons/{comparison_id}", response_model=schemas.Comparison)
def read_comparison(comparison_id: int, db: Session = Depends(get_db)):
    db_comparison = crud.get_comparison(db, comparison_id=comparison_id)
    if db_comparison is None:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return db_comparison

@app.get("/comparisons/", response_model=list[schemas.Comparison])
def read_comparisons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comparisons = crud.get_comparisons(db, skip=skip, limit=limit)
    return comparisons
