from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from aiogram.types import InputFile
from asgiref.sync import sync_to_async


@sync_to_async
def get_drawn_img(img_file: BytesIO) -> InputFile:
    img: Image.Image = Image.open(img_file)
    draw = ImageDraw(img)
    fnt = ImageFont.truetype("DejaVuSans.ttf", 70)

    draw.line((0, 0, 0, img.size[1]), width=12, fill=65280)
    draw.text((15, 0), str(0), font=fnt, fill=65280)
    draw.text((15, img.size[1] - 70), str(img.size[1]), font=fnt, fill=65280)

    drawn_img_file = BytesIO()
    img.save(drawn_img_file, format="png")
    drawn_img_file.seek(0)

    return InputFile(drawn_img_file)


@sync_to_async
def get_separated_imgs(img_file: BytesIO, start, middle, end) -> tuple:
    img: Image.Image = Image.open(img_file)

    for param in (start, middle, end):
        if param > img.size[1] or param < 0:
            return None, None

    word_img_file, transl_img_file = BytesIO(), BytesIO()

    img.crop((0, start, img.size[0], middle)).save(word_img_file, format="png")
    img.crop((0, middle, img.size[0], end)).save(transl_img_file, format="png")

    word_img_file.seek(0)
    transl_img_file.seek(0)

    return InputFile(word_img_file), InputFile(transl_img_file)

