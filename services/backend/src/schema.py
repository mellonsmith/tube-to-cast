from pydantic import BaseModel


class VideoCreate(BaseModel):
    url: str
