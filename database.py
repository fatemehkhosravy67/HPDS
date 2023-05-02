from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./hpds.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class RAMUsage(Base):
    __tablename__ = "ram_usage"
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    free = Column(Float)
    used = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Defining the session retrieval function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
