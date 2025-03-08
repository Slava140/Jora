from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from actors import postprocess_file_actor
from api.v1.projects.services import TaskService
from config import settings
from errors import AppError
from media.schemas import ReadMediaS, ReadMediaWithFilepathS, MediaMetadataS, CreateMediaS
from media.dao import MediaDAO
from utils import decompress_text


class MediaService:
    @classmethod
    def save(cls, file: FileStorage, metadata: MediaMetadataS, compress_it: bool) -> ReadMediaS:
        """
        :except WasNotFoundError
        :except ExtensionsNotAllowedError
        """
        from database import db

        file_path = Path(secure_filename(file.filename))
        extension = file_path.suffix.strip('.')

        media = MediaDAO.add(
            CreateMediaS(filename=file_path.name, **metadata.model_dump())
        )
        task = TaskService.get_one_by_id_or_none(media.task_id)

        try:
            destination_dir = settings.MEDIA_PATH / f'project_id_{task.project_id}' / f'task_id_{task.id}'
            destination_dir.mkdir(exist_ok=True, parents=True)

            destination_path = destination_dir / f'{media.id}.{extension}'
            file.save(destination_path)
            db.session.commit()
        except:
            db.session.rollback()
            raise

        postprocess_file_actor.send(file=str(destination_path), remove_original=compress_it)
        return media

    @classmethod
    def get_media_by_id_or_none(cls, media_id: int) -> ReadMediaWithFilepathS | None:
        metadata = MediaDAO.get_one_by_id_or_none(media_id)
        if metadata is None:
            return None

        task = TaskService.get_one_by_id_or_none(metadata.task_id)

        project_path = settings.MEDIA_PATH / Path(f'project_id_{task.project_id}')
        task_path = project_path / Path(f'task_id_{task.id}')

        file_extension = Path(metadata.filename).suffix.strip('.')
        filepath = task_path / Path(f'{media_id}.{file_extension}')

        if not filepath.exists():
            compressed_file = Path(f'{filepath}.gz')
            if compressed_file.exists():
                decompress_text(compressed_file)
            else:
                return None

        return ReadMediaWithFilepathS(filepath=filepath, **metadata.model_dump())
