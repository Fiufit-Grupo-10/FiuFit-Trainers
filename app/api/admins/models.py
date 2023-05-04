from sqlalchemy import Column, String
from app.config.database import Base


class Admin(Base):
    __tablename__ = "admins"

    uid = Column(String(length=50), unique=True, primary_key=True, index=True)
    email = Column(String(length=100), unique=True, index=True)
    username = Column(String(length=50), unique=True, index=True)
