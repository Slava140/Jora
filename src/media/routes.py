from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_openapi3 import APIBlueprint

from errors import FileIsNotAttachedError, WasNotFoundError
from media.schemas import MediaQS, CreateMediaS
from media.services import MediaService
from security import security


router = APIBlueprint(name='media', import_name=__name__, url_prefix='/media', abp_security=security)


@router.post('/')
@jwt_required()
def add_media(query: MediaQS):
    author_id = get_jwt_identity()

    file = next((file for file in request.files.values()), None)
    if file is None:
        raise FileIsNotAttachedError

    media_metadata = MediaService.save(
        file,
        CreateMediaS(
            filename=file.filename,
            author_id=author_id,
            task_id=query.task_id
        )
    )

    return jsonify(media_metadata.model_dump()), 200


@router.get('/<int:media_id>/')
@jwt_required()
def get_all_media_from_task(media_id: int):
    media_metadata = MediaService.get_media_by_id_or_none(media_id)
    if media_metadata is None:
        raise WasNotFoundError(f'Media with id {media_id}')
    return send_file(media_metadata.filepath, download_name=media_metadata.filename)
