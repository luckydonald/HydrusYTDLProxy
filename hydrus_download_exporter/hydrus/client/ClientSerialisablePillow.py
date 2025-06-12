# ok, the serialised png format is:

# the png is monochrome, no alpha channel (mode 'L' in PIL)
# the data is read left to right in visual pixels. one pixel = one byte
# first two bytes (i.e. ( 0, 0 ) and ( 1, 0 )), are a big endian unsigned short (!H), and say how tall the header is in number of rows. the actual data starts after that
# first four bytes of data are a big endian unsigned int (!I) saying how long the payload is in bytes
# read that many pixels after that, you got the payload
# it should be zlib compressed these days and is most likely a dumped hydrus serialisable object, which is a json guy with a whole complicated loading system. utf-8 it into a string and you are half way there :^)

from PIL import Image, ImageDraw, ImageFont
import struct
import numpy as np
from hydrus.core import HydrusPaths, HydrusTemp

def create_top_image_pillow(width, title, payload_description, text):
    # Load a default font
    font_path = "ChicagoFLF.ttf"  # Adjust for platform
    font_base = ImageFont.truetype(font_path, 16)
    font_payload = ImageFont.truetype(font_path, int(16 * 1.4))
    font_title = ImageFont.truetype(font_path, int(16 * 2.0))

    def get_text_size(draw, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def wrap_text(draw, text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            w, h = get_text_size(draw, test_line, font)
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    # Create dummy image to measure text
    dummy = Image.new("L", (width, 1), 255)
    draw = ImageDraw.Draw(dummy)

    total_height = 6
    text_blocks = []

    for text, font in [(title, font_title), (payload_description, font_payload), (text, font_base)]:
        lines = wrap_text(draw, text, font, width - 20)
        line_height = get_text_size(draw, "A", font)[1]
        y_offset = total_height + 10
        lines_with_pos = [(line, y_offset + i * (line_height + 4)) for i, line in enumerate(lines)]
        total_height = lines_with_pos[-1][1] + line_height + 6 if lines_with_pos else total_height
        text_blocks.append((lines_with_pos, font))

    # Create the actual image
    image = Image.new("L", (width, total_height), 255)
    draw = ImageDraw.Draw(image)

    for lines_with_pos, font in text_blocks:
        for line, y in lines_with_pos:
            w, _ = get_text_size(draw, line, font)
            x = (width - w) // 2
            draw.text((x, y), line, font=font, fill=0)

    # Encode top height in the first 2 pixels
    top_height_bytes = struct.pack('!H', total_height)
    px = image.load()
    px[0, 0] = top_height_bytes[0]
    px[1, 0] = top_height_bytes[1]

    return image


def dump_to_png_pillow(width, payload_bytes, title, payload_description, text, path):
    payload_len = len(payload_bytes)
    full_payload = struct.pack('!I', payload_len) + payload_bytes

    payload_rows = (len(full_payload) + width - 1) // width
    padded_payload = full_payload + b'\x00' * (payload_rows * width - len(full_payload))
    payload_array = np.frombuffer(padded_payload, dtype=np.uint8).reshape((payload_rows, width))

    payload_image = Image.fromarray(payload_array, mode="L")
    top_image = create_top_image_pillow(width, title, payload_description, text)

    final_image = Image.new("L", (width, top_image.height + payload_image.height))
    final_image.paste(top_image, (0, 0))
    final_image.paste(payload_image, (0, top_image.height))
    final_image = final_image.convert("RGBA")  # Convert to RGBA for saving as PNG
    final_image.save(path, format="PNG", compress_level=9)
