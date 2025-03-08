import gzip
import shutil
from pathlib import Path

from config import settings


def compress_text(file: Path):
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix == '.gz':
        raise ValueError('File is already compressed.')

    if file.suffix.strip('.') not in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        raise ValueError(f'File {file.name} is not text file.')

    with open(file, 'rb') as f_plain:
        with gzip.open(f'{file}.gz', 'wb') as f_compressed:
            shutil.copyfileobj(f_plain, f_compressed)


def decompress_text(compressed_file: Path):
    if not compressed_file.is_file():
        raise ValueError('compressed_file argument is not a file.')

    if compressed_file.suffix != '.gz':
        raise ValueError('File is not compressed.')

    plain_file_path = Path(str(compressed_file).strip('.gz'))
    with gzip.open(compressed_file, 'rb') as f_compressed:
        with open(plain_file_path, 'wb') as f_plain:
            shutil.copyfileobj(f_compressed, f_plain)
