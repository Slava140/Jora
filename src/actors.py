import os
from pathlib import Path

from app import dramatiq
from config import settings
from utils import compress_text, compress_image

broker = dramatiq.broker


@dramatiq.actor()
def postprocess_file_actor(file: str, remove_original: bool = True):
    file = Path(file)
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix.strip('.') in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        compress_text(file)
        os.remove(file)

    if file.suffix.strip('.') in settings.ALLOWED_IMAGE_FILE_EXTENSIONS:
        compress_image(file)
        if remove_original:
            os.remove(file)
