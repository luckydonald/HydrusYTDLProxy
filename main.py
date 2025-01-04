import json
from mimetypes import guess_type
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse, urlencode

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

from utils.dates import epoch_to_iso
from utils.misc import default
from utils.types import guess_mime

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
    'quiet': False,
    'nooverwrites': True,
    'writethumbnail': True,
    'writeinfojson': True,
}

FORMATS_TYPE = Literal["mp4", "mp3", "mkv", "webm", "best"]

# noinspection PyUnresolvedReferences
FORMATS_TYPE_STRINGS: tuple[FORMATS_TYPE] = FORMATS_TYPE.__args__

class Thumbnail(BaseModel):
    url: str
    preference: int | None = None
    id: str | None = None
    height: int | None = None
    width: int | None = None
    resolution: str | None = None

class Format(BaseModel):
    format: FORMATS_TYPE
    mime: str
    original_ext: str
    original_mime: str
    url: str

class MetaResponseModel(BaseModel):
    title: str | None = None
    description: str | None = None
    date: int | str | None = None
    tags: list[str] | None = None
    duration: int | None = None
    thumbnails: list[Thumbnail] | None = None
    formats: list[Format]
    width: int | None = None
    height: int | None = None
    meta: dict

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
# end def


# noinspection PyShadowingBuiltins
@app.get("/download-stream")
def download_stream(
    url: str,
    format: FORMATS_TYPE = "mp4",
):
    def progress_hook(d: dict):
        if d['status'] == 'downloading':
            print(f"Downloading: {d['filename']} | Progress: {d['downloaded_bytes'] / d['total_bytes'] * 100:.2f}%")
        # end def
    # end def

    current_config = ydl_opts.copy()
    current_config["format"] = "bestvideo+bestaudio/best"
    # noinspection PyTypeChecker
    current_config['progress_hooks'] = [progress_hook]
    if format != "best":
        current_config["postprocessors"].append(
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format,
            }
        )
    # end if

    with YoutubeDL(ydl_opts) as ydl:
        outer_info = ydl.extract_info(url, download=False)
    # end if
    mime = guess_type(f'filename.{outer_info.get("ext", format)}')[0]

    """Download a URL and stream the requested format."""
    def stream_video():
        yield ""
        with TemporaryDirectory() as tmpdir:
            print('created temporary directory', tmpdir)
            tmpdir = Path(tmpdir).absolute()
            current_config['temp_dir'] = str(tmpdir)
            current_config['outtmpl'] = str(tmpdir / '%(title)s.%(ext)s')

            with YoutubeDL(ydl_opts) as ydl:
                try:
                    # noinspection PyShadowingNames
                    info = ydl.extract_info(url, download=True)
                    yield ""
                    print(repr(info))
                    file_name = ydl.prepare_filename(info)
                    yield ""

                    # Adjust file extension if necessary
                    if format != "best" and not file_name.endswith(f".{format}"):
                        base_name, _ = os.path.splitext(file_name)
                        file_name = f"{base_name}.{format}"
                    # end if
                except Exception:
                    ydl.params["format"] = "bestvideo+bestaudio/best"
                    info = ydl.extract_info(url, download=True)
                    file_name = ydl.prepare_filename(info)
                # end try
            # end with
            try:
                with open(file_name, "rb") as f:
                    yield from f
                # end with
            finally:
                os.remove(file_name)
            # end if
        # end with
    # end def

    return StreamingResponse(stream_video(), media_type=mime)
# end def


@app.get("/meta", response_model=MetaResponseModel)
def meta_about_url(url: str):
    """Get metadata about the given URL."""
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        # end with

        # noinspection PyShadowingBuiltins
        formats: list[Format] = [
            Format(
                format=str(format),
                mime=default(
                    value=guess_mime(ext=format),
                    default=original_mime,
                ),
                original_ext=info.get("ext"),
                original_mime=original_mime,
                url=f"/download-stream?{urlencode(dict(url=url, format=format))!s}",
            )
            for original_mime, format in [
                # tuple (original_mime, format):
                (
                    # original_mime:
                    default(
                        value=guess_mime(ext=info.get("ext", format)),
                        default="audio/mpeg" if format == "mp3" else "video/mp4" if format == "best" else f"video/{format}"
                    ),
                    # format:
                    format,
                )
                for format in FORMATS_TYPE_STRINGS
            ]
        ]
        print(formats)

        parsed_url = urlparse(url)
        tags = [
            "downloader:hydrus_ytdl_proxy",
            f"hydrus_ytdl_proxy:domain:{parsed_url.hostname.removeprefix('www.')}",
            f"hydrus_ytdl_proxy:extractor:{info.get('extractor')}",
            *info.get("tags", []),
            *[f"category:{category}" for category in info.get("categories", [])],
        ]

        return MetaResponseModel(
            title=info.get("title"),
            description=info.get("description"),
            upload_timestamp=epoch_to_iso(info.get("timestamp")),
            fetch_timestamp=epoch_to_iso(info.get("epoch")),
            tags=tags,
            duration=info.get("duration"),
            thumbnails=info.get("thumbnails"),
            width=info.get("width"),
            height=info.get("height"),
            formats=formats,
            meta=info,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # end try
# end def
