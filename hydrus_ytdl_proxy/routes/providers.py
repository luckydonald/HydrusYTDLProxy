from typing import Annotated

from typing_extensions import Doc

from fastapi import APIRouter
from yt_dlp.extractor import gen_extractor_classes
from pydantic import BaseModel
from ..utils.fully_qualified_name import fqn
from regex_cleaner import clean_regex

router = APIRouter()

class ProviderResponseModel(BaseModel):
    all: dict[str, list[str]]
    normalized: dict[str, list[str]]
    regex: dict[str, str]
# end class

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
@router.get("/providers", response_model=ProviderResponseModel)
def list_providers():
    """Get a list of domain names for all sites supported by yt-dlp."""

    providers: dict[str, list[Annotated[str, Doc('regex')]]] = {}
    for cls in gen_extractor_classes():
        if fqn(cls) == 'yt_dlp.extractor.generic.GenericIE' or cls.__name__ == 'GenericIE':
            continue
        # end if
        valid_url = cls._VALID_URL
        if valid_url is False:
            continue
        if isinstance(valid_url, (list, tuple)):
            providers[cls.IE_NAME] = flatten_providers(valid_url)
        else:
            assert isinstance(valid_url, str)
            providers[cls.IE_NAME] = [valid_url]
        # end if
        if any(".*" in value for value in providers.values()):
            raise ValueError(f"Invalid Regex '.*' in provider {fqn(cls)} ")
        # end if
    # end for

    better_providers = {k: [clean_regex(regex) for regex in v] for k, v in providers.items()}
    providers_merged = {k: "|".join(v) for k, v in better_providers.items()}

    return ProviderResponseModel(
        all=providers,
        normalized=better_providers,
        regex=providers_merged,
    )
# end def