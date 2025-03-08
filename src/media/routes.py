from flask import jsonify, send_file
from flask_openapi3 import APIBlueprint, Tag
from flask_security import roles_accepted, current_user

from errors import WasNotFoundError
from media.schemas import MediaMetadataS, UploadMediaS, MediaPath
from media.services import MediaService
from global_schemas import security_schemas
from security import jwt_required

router = APIBlueprint(
    name='media', import_name=__name__, url_prefix='/media',
    abp_security=security_schemas, abp_tags=[Tag(name='Media')]
)


@router.post('/')
@jwt_required()
@roles_accepted('admin', 'user')
def add_media(form: UploadMediaS):
    metadata = MediaService.save(
        file=form.file,
        metadata=MediaMetadataS(
            author_id=current_user.id,
            task_id=form.task_id
        ),
        compress_it=form.compress_it
    )
    return jsonify(metadata.model_dump()), 201


@router.get('/<int:media_id>/')
@jwt_required()
@roles_accepted('admin', 'user')
def get_media_by_id(path: MediaPath):
    metadata = MediaService.get_media_by_id_or_none(path.media_id)
    if metadata is None:
        raise WasNotFoundError(f'Media with id {path.media_id}')
    return send_file(metadata.filepath, download_name=metadata.filename)
