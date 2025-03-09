from hydrus.client import ClientSerialisable

from serializer_foo_two import generate_stuff_payload, PROVIDED_SERVICES_IDS
from serializer_foo_patch import patch


def run(
    width=512,
    title="Downlaoder",
    payload_description="Automatically generated payload",
    text="",
    path="/Users/user/git/hydrusnetwork/hydrus/EXPORT/GENERATED.png",
    host='hcydrus-ytdl-proxy-u0g0sw4cwwk4s8o8g84ksw0g.c1.bn-x.de',
    proto = 'https',
):
    payload = generate_stuff_payload(host, proto, services=PROVIDED_SERVICES_IDS)#
    (payload_bytes, payload_length) = ClientSerialisable.GetPayloadBytesAndLength(payload)
    patch()
    ClientSerialisable.DumpToPNG( width, payload_bytes, title, payload_description, text, path )
# end def


if __name__ == "__main__":
    run()
