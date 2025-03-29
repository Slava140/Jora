import os
from pathlib import Path
from smtplib import SMTPException

from flask import render_template

from security import security
from api.v1.projects.services import TaskService, ProjectService
from app import dramatiq
from config import settings
from utils import compress_text, compress_image, Mail

broker = dramatiq.broker


@dramatiq.actor(max_retries=0)
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


def should_retry_notification_actor(retries, exception):
    return retries < 3 and isinstance(exception, SMTPException)


@dramatiq.actor(
    retry_when=should_retry_notification_actor,
    min_backoff=60_000,
    max_backoff=10*60_000,
    time_limit=20_000
)
def send_notification_actor(
        recipient_user_id: int,
        subject: str,
        task_id: int,
        task_url: str,
        template_name: str = 'notification.html'
):
    recipient = security.datastore.find_user(id=recipient_user_id)
    task = TaskService.get_one_by_id_or_none(task_id)
    project = ProjectService.get_one_by_id_or_none(task.project_id)

    if task.due_date:
        due_date_str = task.due_date.strftime('%d.%m.%Y %X (%Z)')
    else:
        due_date_str = 'Не указано'

    email_content = render_template(
        template_name,
        header=subject,
        task_status=task.status,
        task_title=task.title,
        due_date=due_date_str,
        project_title=project.title,
        task_url=task_url
    )
    mail = Mail()
    mail.send(recipient=recipient.email, subject=subject, content=email_content, content_type='html')
