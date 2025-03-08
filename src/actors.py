import os
from pathlib import Path

from app import dramatiq
from config import settings
from utils import compress_text

broker = dramatiq.broker


@dramatiq.actor()
def postprocess_file_actor(file: str, remove_original: bool = False):
    file = Path(file)
    if file.suffix.strip('.') in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        compress_text(file)

        if remove_original:
            os.remove(file)
