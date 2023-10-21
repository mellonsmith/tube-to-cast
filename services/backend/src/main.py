from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # NEW
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Video
from .schema import VideoCreate
import os
import yt_dlp
import podgen
import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/download/")
def download_video(video: VideoCreate, db: Session = Depends(get_db)):
    try:
        with yt_dlp.YoutubeDL({'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]', 'outtmpl': 'downloads/%(title)s.%(ext)s'}) as ydl:
            info_dict = ydl.extract_info(video.url, download=True)
            video_file = ydl.prepare_filename(info_dict)
    except:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    file_size = os.path.getsize(video_file)
    db_video = Video(title=info_dict['title'], description=info_dict['description'], url=video.url,
                     file_path=video_file, thumbnail_url=info_dict['thumbnail'], filesize=file_size)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    return {"message": "Video downloaded and added to database"}


@app.get("/videos/")
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos


@app.delete("/videos/{video_id}")
def del_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    os.remove(video.file_path)
    db.delete(video)
    db.commit()
    return {"message": "Video deleted"}


@app.get("/podcast/")
def generate_podcast(db: Session = Depends(get_db)):
    # Create a new Podcast object
    podcast = podgen.Podcast()

    # Set the podcast metadata
    podcast.name = "My Awesome Podcast"
    podcast.description = "A podcast about awesome things"
    podcast.website = "https://example.com/podcast"
    podcast.explicit = False

    # Add each video to the podcast as an episode
    for video in db.query(Video).all():
        episode = podcast.add_episode()
        episode.title = video.title
        episode.summary = video.description
        episode.thumbnail = video.thumbnail_url

        episode.media = podgen.Media(video.file_path, type="video/webm")
        episode.length = video.filesize
        episode.image = video.thumbnail_url

    # Generate the RSS feed and return it as a string
    with open("feed.rss", "w") as f:
        f.write(podcast.rss_str())

    return "Podcast updated"
