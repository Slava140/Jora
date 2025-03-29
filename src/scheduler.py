from flask_apscheduler import APScheduler

from api.v1.projects.schemas import CreateTaskS, CreateCommentS
from api.v1.projects.services import TaskService, CommentService
from utils import Mail

scheduler = APScheduler()


@scheduler.task('interval', seconds=60)
def get_mail_job():
    mail = Mail()
    tasks = mail.read()
    with scheduler.app.app_context():
        for task_from_email in tasks:
            task_schema = CreateTaskS(**task_from_email.model_dump())
            created_task = TaskService.add(task_schema)
            mail.mark_as_read(task_from_email.email_uid)
            comment_schema = CreateCommentS(
                content=f'Отправлено пользователем {task_from_email.email_author}',
                task_id=created_task.id,
                author_id=created_task.author_id
            )
            CommentService.add(comment_schema)
