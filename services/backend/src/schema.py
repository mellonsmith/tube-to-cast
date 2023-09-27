from typing import List
from pydantic import BaseModel


class VideoBase(BaseModel):
    id: int
    title: str
    description: str
    url: str
    file_path: str
    thumbnail_url: str
    filesize: int


class VideoCreate(VideoBase):
    pass


class VideoDelete(BaseModel):
    id: int


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True


class VideoList(BaseModel):
    videos: List[Video]
