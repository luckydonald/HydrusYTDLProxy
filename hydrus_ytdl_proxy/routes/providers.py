from fastapi import APIRouter
from yt_dlp.extractor import gen_extractor_classes
from pydantic import BaseModel
from ..utils.fully_qualified_name import fqn
from ..utils.dates import epoch_to_iso
from ..utils.misc import default
from ..utils.types import guess_mime
from regex_cleaner import clean_regex

router = APIRouter()

class ProviderResponseModel(BaseModel):
    all: list[str]
    normalized: list[str]
    regex: str
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

    providers = []
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
        if ".*" in providers:
            raise ValueError(f"Invalid Regex '.*' in provider {fqn(cls)} ")
        # end if
    # end for

    better_providers = [clean_regex(provider) for provider in providers]
    providers_merged = "|".join(better_providers)

    return ProviderResponseModel(
        all=providers,
        normalized=better_providers,
        regex=providers_merged,
    )
# end def