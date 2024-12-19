import os.path
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.v1.projects.services import TaskService
from config import settings
from media.schemas import ReadMediaS, ReadMediaWithFilepathS, CreateMediaS
from media.dao import MediaDAO

from errors import WasNotFoundError, ExtensionsNotAllowedError, MustBePositiveError


class MediaService:
    @classmethod
    def __get_file_extensions(cls, filename: str) -> str:
        if '.' not in filename:
            return 'No extension'
        return filename.rsplit('.', 1)[1].lower()

    @classmethod
    def save(cls, file: FileStorage, media_metadata: CreateMediaS) -> ReadMediaS:
        """
        :except WasNotFoundError
        :except ExtensionsNotAllowedError
        """
        filename = secure_filename(file.filename)
        file_extension = cls.__get_file_extensions(filename)

        if file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
            raise ExtensionsNotAllowedError(file_extension)

        media = MediaDAO.add(media_metadata)
        task = TaskService.get_one_by_id_or_none(media.task_id)

        project_media_dir = (settings.MEDIA_PATH / f'project_id_{task.project_id}')
        project_media_dir.mkdir(exist_ok=True)

        task_media_dir = (project_media_dir / f'task_id_{task.id}')
        task_media_dir.mkdir(exist_ok=True)

        file.save(task_media_dir / f'{media.id}.{file_extension}')

        return media

    @classmethod
    def get_media_by_id_or_none(cls, media_id: int) -> ReadMediaWithFilepathS | None:
        media_metadata = MediaDAO.get_one_by_id_or_none(media_id)
        if media_metadata is None:
            return None

        extension = cls.__get_file_extensions(media_metadata.filename)
        task = TaskService.get_one_by_id_or_none(media_metadata.task_id)
        filepath = settings.MEDIA_PATH / Path(f'project_id_{task.project_id}/task_id_{task.id}/{media_id}.{extension}')

        if not filepath.exists():
            return None

        return ReadMediaWithFilepathS(filepath=filepath, **media_metadata.model_dump())
