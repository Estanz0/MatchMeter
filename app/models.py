from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    input1 = Column(String, index=True)
    input2 = Column(String, index=True)
    in_common = Column(String)
    not_in_common = Column(String)
    score = Column(Float)
