import os.path
from os import makedirs
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.v1.projects.services import TaskService
from config import settings
from media.schemas import ReadMediaS, ReadMediaWithFilepathS, MediaMetadataS, CreateMediaS
from media.dao import MediaDAO

from errors import WasNotFoundError, ExtensionsNotAllowedError, MustBePositiveError


class MediaService:
    @classmethod
    def __get_file_extensions(cls, filename: str) -> str | None:
        if '.' not in filename.strip('.'):
            return None
        return filename.rsplit('.', 1)[1].lower()

    @classmethod
    def save(cls, file: FileStorage, metadata: MediaMetadataS) -> ReadMediaS:
        """
        :except WasNotFoundError
        :except ExtensionsNotAllowedError
        """
        filename, extension = os.path.splitext(secure_filename(file.filename))
        extension = extension.strip('.')

        media = MediaDAO.add(
            CreateMediaS(filename=filename, extension=extension, **metadata.model_dump())
        )
        task = TaskService.get_one_by_id_or_none(media.task_id)

        destination_dir = settings.MEDIA_PATH / f'project_id_{task.project_id}' / f'task_id_{task.id}'
        makedirs(destination_dir, exist_ok=True)

        file.save(destination_dir / f'{media.id}.{extension}')

        return media

    @classmethod
    def get_media_by_id_or_none(cls, media_id: int) -> ReadMediaWithFilepathS | None:
        metadata = MediaDAO.get_one_by_id_or_none(media_id)
        if metadata is None:
            return None

        task = TaskService.get_one_by_id_or_none(metadata.task_id)
        project_path = settings.MEDIA_PATH / Path(f'project_id_{task.project_id}')
        task_path = project_path / Path(f'task_id_{task.id}')
        filepath = task_path / Path(f'{media_id}.{metadata.extension}')

        if not filepath.exists():
            return None

        return ReadMediaWithFilepathS(filepath=filepath, **metadata.model_dump())
