from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
from yt_dlp import YoutubeDL
from yt_dlp.extractor import gen_extractor_classes
from yt_dlp.postprocessor.embedthumbnail import EmbedThumbnailPP
from yt_dlp.postprocessor.ffmpeg import FFmpegMetadataPP, FFmpegEmbedSubtitlePP

import os
from typing import List, Optional

os.environ['YTDLP_NO_LAZY_EXTRACTORS'] = '1'

app = FastAPI()

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "%(id)s.%(ext)s",
    "noplaylist": True,
    "postprocessors": [
        {"key": "FFmpegEmbedSubtitle"},
        {"key": "FFmpegMetadata"},
        {"key": "EmbedThumbnail"},
    ],
}

class MetaResponseModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    duration: Optional[int]
    thumbnails: Optional[List[dict]]
    formats: List[dict]

@app.get("/providers", response_model=List[str])
def list_providers():
    """Get a list of domain names for all sites supported by yt-dlp."""
    providers = []
    for cls in gen_extractor_classes():
        valid_url = cls._VALID_URL
        if valid_url is False:
            continue
        if isinstance(valid_url, list):
            providers.extend(valid_url)
        else:
            providers.append(valid_url)
    return providers

@app.post("/download-stream")
def download_stream(
    url: str, format: Optional[str] = Query("mp4", regex="^(mp4|mp3|mkv|webm)$")
):
    """Download a URL and stream the requested format."""
    def stream_video():
        with YoutubeDL({**ydl_opts, "postprocessor_args": ["-f", format]}) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
        with open(file_name, "rb") as f:
            yield from f
        os.remove(file_name)

    return StreamingResponse(stream_video(), media_type=f"video/{format}")

@app.get("/meta", response_model=MetaResponseModel)
def meta_about_url(url: str):
    """Get metadata about the given URL."""
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = [
            {"format": "mkv", "url": f"/download-stream?url={url}&format=mkv"},
            {"format": "webm", "url": f"/download-stream?url={url}&format=webm"},
            {"format": "mp4", "url": f"/download-stream?url={url}&format=mp4"},
            {"format": "mp3", "url": f"/download-stream?url={url}&format=mp3"},
        ]

        return MetaResponseModel(
            title=info.get("title"),
            description=info.get("description"),
            tags=info.get("tags"),
            duration=info.get("duration"),
            thumbnails=info.get("thumbnails"),
            formats=formats,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
