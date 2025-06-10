import tempfile

from hydrus.client import ClientSerialisable

from serializer_foo_two import generate_stuff_payload, PROVIDED_SERVICES_IDS
from serializer_foo_patch import patch


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
    (payload_bytes, payload_length) = ClientSerialisable.GetPayloadBytesAndLength(payload)
    patch()
    ClientSerialisable.DumpToPNG( width, payload_bytes, title, payload_description, text, path )
# end def


if __name__ == "__main__":
    run()
