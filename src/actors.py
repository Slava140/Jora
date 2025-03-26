import os
from pathlib import Path

from flask import render_template

from security import security
from api.v1.projects.services import TaskService, ProjectService
from app import dramatiq
from config import settings
from utils import compress_text, compress_image, send_email

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


@dramatiq.actor()
def send_notification_about_appointment_as_assignee_actor(
        assignee_id: int,
        task_id: int,
        task_url: str,
        subject: str = 'Вы назначены исполнителем.',
        template_name: str = 'assignee_changed.html'
):
    assignee = security.datastore.find_user(id=assignee_id)
    task = TaskService.get_one_by_id_or_none(task_id)
    project = ProjectService.get_one_by_id_or_none(task.project_id)

    if task.due_date:
        due_date_str = task.due_date.strftime('%d.%m.%Y %X (%Z)')
    else:
        due_date_str = 'Не указано'

    email_content = render_template(
        template_name,
        task_status=task.status,
        task_title=task.title,
        due_date=due_date_str,
        project_title=project.title,
        task_url=task_url
    )
    send_email(recipient=assignee.email, subject=subject, content=email_content, content_type='html')
