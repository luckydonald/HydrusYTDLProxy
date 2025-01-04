from functools import lru_cache
from mimetypes import guess_type


@lru_cache
def guess_mime(*, ext: str) -> str | None:
    return guess_type(f'filename.{ext}')[0]
# end def
