from sqlalchemy import Column, String, Text
from app.config.database import Base


class TrainingType(Base):
    __tablename__ = "trainingtypes"

    name = Column(String(length=50), primary_key=True, unique=True, index=True)
    descr = Column(Text)
