import json

from pydantic import BaseModel, ValidationError
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
from yt_dlp import YoutubeDL
from yt_dlp.extractor import gen_extractor_classes
from yt_dlp.postprocessor.embedthumbnail import EmbedThumbnailPP
from yt_dlp.postprocessor.ffmpeg import FFmpegMetadataPP, FFmpegEmbedSubtitlePP
import os
from typing import Literal

from pydantic import BaseModel
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

FORMATS_TYPE = Literal["mp4", "mp3", "mkv", "webm", "best"]

class Thumbnail(BaseModel):
    url: str
    preference: int | None = None
    id: str | None = None
    height: int | None = None
    width: int | None = None
    resolution: str | None = None

class Format(BaseModel):
    format: FORMATS_TYPE
    url: str

class MetaResponseModel(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    duration: int | None = None
    thumbnails: list[Thumbnail] | None = None
    formats: list[Format]

@app.get("/providers", response_model=list[str])
def list_providers():
    """Get a list of domain names for all sites supported by yt-dlp."""
    def flatten_providers(providers):
        flattened = []
        for item in providers:
            if isinstance(item, str):
                flattened.append(item)
            elif isinstance(item, (list, tuple)):
                flattened.extend(flatten_providers(item))
        return flattened

    providers = []
    for cls in gen_extractor_classes():
        valid_url = cls._VALID_URL
        if valid_url is False:
            continue
        if isinstance(valid_url, (list, tuple)):
            providers.extend(flatten_providers(valid_url))
        else:
            providers.append(valid_url)
    return providers


# noinspection PyShadowingBuiltins
@app.get("/download-stream")
def download_stream(
    url: str,
    format: FORMATS_TYPE = "mp4",
):

    """Download a URL and stream the requested format."""
    def stream_video():
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.params["format"] = "bestvideo+bestaudio/best" if format == "best" else format
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)

                # Adjust file extension if necessary
                if format != "best" and not file_name.endswith(f".{format}"):
                    base_name, _ = os.path.splitext(file_name)
                    file_name = f"{base_name}.{format}"

                # Set appropriate content type
                nonlocal media_type
                media_type = "audio/mpeg" if format == "mp3" else "video/mp4" if format in ["best", "mp4"] else f"video/{format}"
            except Exception:
                ydl.params["format"] = "bestvideo+bestaudio/best"
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)

        with open(file_name, "rb") as f:
            yield from f
        os.remove(file_name)

    media_type = ""
    return StreamingResponse(stream_video(), media_type=media_type)

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
            {"format": "best", "url": f"/download-stream?url={url}&format=best"},
        ]

        return MetaResponseModel(
            title=info.get("title"),
            description=info.get("description"),
            tags=info.get("tags"),
            duration=info.get("duration"),
            thumbnails=info.get("thumbnails"),
            formats=formats,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
