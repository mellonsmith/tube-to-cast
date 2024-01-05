from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Video
from .schema import VideoCreate
import os
import yt_dlp
import pytz
import podgen
import datetime
from dotenv import load_dotenv

load_dotenv("../.env")
base_url = os.getenv("BASE_URL")
frontend_url = os.getenv("FRONTEND_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
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
    # Download video
    try:
        with yt_dlp.YoutubeDL({'format': 'best[ext=m4a]/best[ext=mp4]/best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}) as ydl:
            info_dict = ydl.extract_info(video.url, download=True)
            video_file = ydl.prepare_filename(info_dict)
    except:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # Add video to database
    file_size = os.path.getsize(video_file)
    db_video = Video(title=info_dict['title'], description=info_dict['description'], url=video.url,
                     file_path=video_file, thumbnail_url=info_dict['thumbnail'], filesize=file_size, date=datetime.datetime.now())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    # Update podcast feed
    try:
        generate_podcast(db)
    except:
        raise HTTPException(
            status_code=500, detail="Failed to update podcast feed")

    return {"message": "Video downloaded and added to database"}


@app.get("/videos/")
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos


@app.get("/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(video.file_path, media_type="video/mp4")


@app.delete("/videos/{video_id}")
def del_video(video_id: int, db: Session = Depends(get_db)):
    # Delete video from database
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=422, detail="Video not found")

    os.remove(video.file_path)  # Delete video file
    db.delete(video)
    db.commit()

    # Update podcast feed
    try:
        generate_podcast(db)
    except:
        raise HTTPException(
            status_code=500, detail="Failed to update podcast feed")

    return {"message": "Video deleted"}


@app.get("/podcast/")
def generate_podcast(db: Session = Depends(get_db)):
    # Create a new Podcast object
    podcast = podgen.Podcast()
    timezone = pytz.timezone('Europe/Berlin')
    # Set the podcast metadata
    podcast.name = "Tube to Cast"
    podcast.description = "A podcast with my downloaded Videos"
    podcast.website = frontend_url
    podcast.explicit = False
    podcast.feed_url = base_url + "/feed.rss"

    # Add each video to the podcast as an episode
    for video in db.query(Video).all():
        episode = podcast.add_episode()
        episode.title = video.title
        episode.summary = video.description
        episode.thumbnail = video.thumbnail_url
        episode.publication_date = video.date.astimezone(timezone)

        episode.media = podgen.Media(
            f"{base_url}/videos/{video.id}", type="video/mp4", size=video.filesize)

        episode.length = video.filesize
        episode.image = video.thumbnail_url

    # Generate the RSS feed and return it as a string
    with open("public/feed.rss", "w") as f:
        f.write(podcast.rss_str())

    return "Podcast updated"


@app.get("/feed.rss")
async def serve_rss_feed():
    rss_feed_path = "public/feed.rss"

    return FileResponse(rss_feed_path, media_type="application/rss+xml")
