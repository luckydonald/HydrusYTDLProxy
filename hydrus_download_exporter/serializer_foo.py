import tempfile

from hydrus.client import ClientSerialisable

from .serializer_foo_two import generate_stuff_payload, PROVIDED_SERVICES_IDS
from .serializer_foo_patch import patch


def run(
    width=512,
    title="Downloader",
    payload_description="Automatically generated payload",
    host='hydrus-ytdl-proxy.example.com',
    text="",
    path: str | None = None,
    proto = 'https',
):

    if path is None:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            result = run(width, title, payload_description, host, text, tmpfile.name, proto)
            input(f'Your file is saved to {tmpfile.name!r}. Press Enter to exit.')
            return result
        # end with
    # end if
    payload = generate_stuff_payload(host, proto, services=PROVIDED_SERVICES_IDS)#
    print(f'PREPARED PAYLOAD: {payload!r}')
    (payload_bytes, payload_length) = ClientSerialisable.GetPayloadBytesAndLength(payload)
    print(f'GENERATED PAYLOAD: {payload_bytes=}, {payload_length=}')

    patch()
    print(f'GENERATING IMG: {payload_bytes=}, {payload_length=}')
    ClientSerialisable.DumpToPNG( width, payload_bytes, title, payload_description, text, path )
    print(f'GENERATED IMG: {width=}, {payload_bytes=}, {payload_length=}')
# end def


if __name__ == "__main__":
    run()
