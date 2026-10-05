from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "sqlite:///./traffic.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TrafficEvent(Base):
    __tablename__ = "traffic_events"
    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    violation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
