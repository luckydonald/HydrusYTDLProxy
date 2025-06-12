from typing import Annotated

from typing_extensions import Doc

from fastapi import APIRouter
from yt_dlp.extractor import gen_extractor_classes
from pydantic import BaseModel
from ..utils.fully_qualified_name import fqn
from regex_cleaner import clean_regex

router = APIRouter()

type ProviderRegexStr = Annotated[str, Doc('regex')]

class ProviderRegexes(BaseModel):
    all: list[ProviderRegexStr]
    normalized: list[ProviderRegexStr]
    regex: ProviderRegexStr
# end class


type ProviderResponse = dict[str, ProviderRegexes]


def flatten_providers(providers: list | tuple) -> list[str]:
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


@router.get("/providers", response_model=ProviderResponse)
def list_providers() -> ProviderResponse:
    """Get a list of domain names for all sites supported by yt-dlp."""

    providers: dict[str, ProviderRegexes] = {}
    for cls in gen_extractor_classes():
        if fqn(cls) == 'yt_dlp.extractor.generic.GenericIE' or cls.__name__ == 'GenericIE':
            continue
        # end if
        valid_url = cls._VALID_URL
        if valid_url is False:
            continue
        if isinstance(valid_url, (list, tuple)):
            regexes = flatten_providers(valid_url)
        else:
            assert isinstance(valid_url, str)
            regexes = [valid_url]
        # end if
        if ".*" in regexes:
            raise ValueError(f"Invalid Regex '.*' in provider {fqn(cls)} ")
        # end if
        better_regexes = [clean_regex(regex) for regex in regexes]
        regexes_merged = "|".join(better_regexes)
        providers[cls.IE_NAME] = ProviderRegexes(
            all=regexes,
            normalized=better_regexes,
            regex=regexes_merged,

        )
    # end for
    return providers
# end def