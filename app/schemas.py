from pydantic import BaseModel

class ComparisonBase(BaseModel):
    input1: str
    input2: str

class ComparisonCreate(ComparisonBase):
    pass

class Comparison(ComparisonBase):
    id: int
    score: float
    in_common: str
    not_in_common: str

    class Config:
        from_attributes = True
