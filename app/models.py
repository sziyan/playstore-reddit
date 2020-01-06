from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String, Float
Base = declarative_base()

class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    count = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    price = Column(String, nullable=True)
    category = Column(String, nullable=True)


class Apps(Base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    count = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    price = Column(String, nullable=True)
    category = Column(String, nullable=True)
