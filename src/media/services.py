from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from actors import postprocess_file_actor
from api.v1.projects.services import TaskService
from config import settings
from media.schemas import ReadMediaS, ReadMediaWithFilepathS, MediaMetadataS, CreateMediaS
from media.dao import MediaDAO


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

        task_path = settings.MEDIA_PATH / f'project_id_{task.project_id}' / f'task_id_{task.id}'

        compressed_filepath = task_path / f'compressed_{media_id}'
        compressed_text = compressed_filepath.with_suffix('.gz')
        compressed_image = compressed_filepath.with_suffix('.jpg')

        if compressed_text.exists():
            filepath = compressed_text
        elif compressed_image.exists():
            filepath = compressed_image
        else:
            return None

        return ReadMediaWithFilepathS(filepath=filepath, **metadata.model_dump())
