from sqlalchemy import Column, Integer, String
from .database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    url = Column(String, unique=True, index=True)
    file_path = Column(String)
    thumbnail_url = Column(String)
    filesize = Column(Integer)
