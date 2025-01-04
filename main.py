import re
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse, urlencode

from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from yt_dlp import YoutubeDL
from yt_dlp.extractor import gen_extractor_classes
from yt_dlp.postprocessor.embedthumbnail import EmbedThumbnailPP
from yt_dlp.postprocessor.ffmpeg import FFmpegMetadataPP, FFmpegEmbedSubtitlePP, FFmpegVideoConvertorPP
import os
from typing import Literal

from pydantic import BaseModel

from utils.dates import epoch_to_iso
from utils.fully_qualified_name import fqn
from utils.misc import default
from utils.regexes import normalize_multiline_regex
from utils.types import guess_mime

os.environ['YTDLP_NO_LAZY_EXTRACTORS'] = '1'

app = FastAPI()

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "%(id)s.%(ext)s",
    "noplaylist": True,
    "postprocessors": [
        {"key": clazz.__name__.removesuffix('PP')}
        for clazz in
        (
            FFmpegEmbedSubtitlePP,
            FFmpegMetadataPP,
            EmbedThumbnailPP,
        )
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
# end class


class Format(BaseModel):
    format: FORMATS_TYPE
    mime: str
    original_ext: str
    original_mime: str
    url: str
# end class


class MetaResponseModel(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime | None = None
    date_of_fetch: datetime | None = None
    tags: list[str] | None = None
    duration: int | None = None
    thumbnails: list[Thumbnail] | None = None
    formats: dict[FORMATS_TYPE, Format]
    width: int | None = None
    height: int | None = None
    meta: dict
# end class


class ProviderResponseModel(BaseModel):
    all: list[str]
    normalized: list[str]
    regex: str
# end class


@app.get("/providers", response_model=ProviderResponseModel)
def list_providers():
    """Get a list of domain names for all sites supported by yt-dlp."""
    def flatten_providers(providers):
        flattened = []
        for item in providers:
            if isinstance(item, str):
                flattened.append(item)
            elif isinstance(item, (list, tuple)):
                flattened.extend(flatten_providers(item))
            # end if
        # end for
        return flattened
    # end def

    providers = []
    for cls in gen_extractor_classes():
        if fqn(cls) == 'yt_dlp.extractor.generic.GenericIE' or cls.__name__ == 'GenericIE':
            continue
        # end if
        valid_url = cls._VALID_URL
        if valid_url is False:
            continue
        if isinstance(valid_url, (list, tuple)):
            providers.extend(flatten_providers(valid_url))
        else:
            assert isinstance(valid_url, str)
            providers.append(valid_url)
        # end if
        if ".*" in providers:
            raise ValueError(f"Invalid Regex '.*' in provider {fqn(cls)} ")
        # end if
    # end for

    better_providers = [normalize_multiline_regex(provider) for provider in providers]
    providers_merged = "|".join(better_providers)

    return ProviderResponseModel(
        all=providers,
        normalized=better_providers,
        regex=providers_merged,
    )
# end def


# noinspection PyShadowingBuiltins
@app.get("/dl")
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
    # current_config['progress_hooks'] = [progress_hook]
    if format != "best":
        current_config["postprocessors"].append(
            {
                'key': FFmpegVideoConvertorPP.__name__.removesuffix('PP'),
                'preferedformat': format,
            }
        )
    # end if

    with YoutubeDL(ydl_opts) as ydl:
        outer_info = ydl.extract_info(url, download=False)
        outer_file_name = ydl.prepare_filename(outer_info)
    # end if
    mime = guess_mime(ext=outer_info.get("ext", format))

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
                except Exception:
                    yield ""
                    ydl.params["format"] = "bestvideo+bestaudio/best"
                    info = ydl.extract_info(url, download=True)
                    file_name = ydl.prepare_filename(info)
                # end try
            # end with
            yield ""
            try:
                with open(file_name, "rb") as f:
                    yield from f
                # end with
            finally:
                os.remove(file_name)
            # end if
        # end with
    # end def

    headers = {
        'Content-Disposition': f'attachment; filename="{outer_file_name.replace(""" " """.strip(), """ """)}"',
    }

    return StreamingResponse(stream_video(), headers=headers, media_type=mime)
# end def


@app.get("/meta", response_model=MetaResponseModel)
def meta_about_url(url: str):
    """Get metadata about the given URL."""
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        # end with

        # noinspection PyShadowingBuiltins
        formats: dict[FORMATS_TYPE, Format] = {
            format: Format(
                format=str(format),
                mime=default(
                    value=guess_mime(ext=format),
                    default=original_mime,
                ),
                original_ext=info.get("ext"),
                original_mime=original_mime,
                url=f"{app.url_path_for(download_stream.__name__)}?{urlencode(dict(url=url, format=format))!s}",
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
        }

        parsed_url = urlparse(url)
        tags = [
            "downloader:hydrus_ytdl_proxy",
            f"hydrus_ytdl_proxy.domain:{parsed_url.hostname.removeprefix('www.')}",
            f"hydrus_ytdl_proxy.extractor:{info.get('extractor')}",
            f"hydrus_ytdl_proxy.id:{info.get('id')}",
            f"id:{info.get('extractor')}:{info.get('id')}",
            *info.get("tags", []),
            *[f"category:{category}" for category in info.get("categories", [])],
        ]

        return MetaResponseModel(
            title=info.get("title"),
            description=info.get("description"),
            date=epoch_to_iso(info.get("timestamp")),
            date_of_fetch=epoch_to_iso(info.get("epoch")),
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
