import gzip
import shutil
from pathlib import Path

from PIL import Image

from config import settings


def compress_image(file: Path):
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix.strip('.') not in settings.ALLOWED_IMAGE_FILE_EXTENSIONS:
        raise ValueError(f'File {file.name} is not image.')

    image = Image.open(file).convert('RGB')
    file_dir = file.parent
    image.save(file_dir / f'compressed_{file.stem}.jpg', quality=90)


def compress_text(file: Path):
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix == '.gz':
        raise ValueError('File is already compressed.')

    if file.suffix.strip('.') not in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        raise ValueError(f'File {file.name} is not text file.')

    file_dir = file.parent
    with open(file, 'rb') as f_plain:
        with gzip.open(file_dir / f'compressed_{file.stem}.gz', 'wb') as f_compressed:
            shutil.copyfileobj(f_plain, f_compressed)
