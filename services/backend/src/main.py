from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # NEW
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Video
from .schema import VideoCreate
from pytube import YouTube


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return "Hello, World!"


@app.post("/download/")
def download_video(video: VideoCreate, db: Session = Depends(get_db)):
    try:
        mydownload = YouTube(video.url)
    except:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    video_file = mydownload.streams.get_by_resolution(
        '720p')  # mydownload.streams.get_highest_resolution()
    video_file.download('../downloads')

    db_video = Video(title=mydownload.title, description=mydownload.description, url=video.url,
                     file_path=video_file.default_filename, thumbnail_url=mydownload.thumbnail_url, filesize=video_file.filesize)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    return {"message": "Video downloaded and added to database"}
