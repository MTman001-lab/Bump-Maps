from sqlalchemy import create_engine, Column, String, Float, Integer, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

Base = declarative_base()

class BumpState(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"

class Bump(Base):
    __tablename__ = "bumps"
    id = Column(String, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    auto_count = Column(Integer, default=0)
    manual_add_count = Column(Integer, default=0)
    manual_remove_count = Column(Integer, default=0)
    state = Column(Enum(BumpState), default=BumpState.PENDING)

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
