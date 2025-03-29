import email
import gzip
import imaplib
import shutil
import string
from base64 import b64decode
from contextlib import contextmanager
from email.header import decode_header
from email.message import Message
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import SMTP
from typing import Literal

from PIL import Image

from api.v1.projects.models import Status
from api.v1.projects.schemas import CreateTaskFromEmailS
from config import settings


def compress_image(file: Path):
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix.strip('.') not in settings.ALLOWED_IMAGE_FILE_EXTENSIONS:
        raise ValueError(f'File {file.name} is not image.')

    image = Image.open(file).convert('RGB')
    file_dir = file.parent
    image.save(file_dir / f'compressed_{file.stem}.jpg', quality=90)


def compress_text(file: Path):
    if not file.is_file():
        raise ValueError('file argument is not a file.')

    if file.suffix == '.gz':
        raise ValueError('File is already compressed.')

    if file.suffix.strip('.') not in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        raise ValueError(f'File {file.name} is not text file.')

    file_dir = file.parent
    with open(file, 'rb') as f_plain:
        with gzip.open(file_dir / f'compressed_{file.stem}.gz', 'wb') as f_compressed:
            shutil.copyfileobj(f_plain, f_compressed)


class Mail:
    def __init__(self, user: str | None = None, password: str | None = None):
        self.__user = user or settings.MAIL_USER
        self.__password = password or settings.MAIL_PASS

    def send(self, recipient: str, subject: str, content: str, content_type: Literal['plain', 'html']) -> None:
        message = MIMEText(content, content_type)
        message['Subject'] = subject

        with SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(self.__user, self.__password)
            server.sendmail(self.__user, recipient, message.as_string())

    @contextmanager
    def __imap_session(self, readonly: bool = True):
        mail = imaplib.IMAP4_SSL(settings.MAIL_HOST)
        mail.login(self.__user, self.__password)
        mail.select(settings.READ_MAILBOX, readonly=readonly)
        yield mail
        mail.logout()

    def __get_messages(self, search_arg: str, mark_as_read: bool) -> list[tuple[int, Message]]:
        result = []
        with self.__imap_session(readonly=not mark_as_read) as mail:
            _, (uids,) = mail.uid('search', search_arg)
            uids = uids.split(b' ') if uids else []
            for uid in uids:
                _, ((_, content), *_) = mail.uid('fetch', uid, '(RFC822)')
                message = email.message_from_bytes(content)
                result.append((int(uid.decode()), message))
        return result

    def mark_as_read(self, message_uid: int | str | bytes) -> None:
        uid = str(message_uid).encode()
        with self.__imap_session(readonly=False) as mail:
            mail.uid('store', uid, '+FLAGS', '\\Seen')

    def read(self, search_arg: str = 'UNSEEN', mark_as_read: bool = False) -> list[CreateTaskFromEmailS]:
        emails: list[CreateTaskFromEmailS] = []
        messages = self.__get_messages(search_arg, mark_as_read)

        for uid, message in messages:
            # Достаю тему письма, если она указана иначе None
            subject = message['Subject']
            subject: str | None = decode_header(subject)[0][0].decode().strip() if subject else None

            # Если тема письма отсутствует или не начинается с "жалоба" перехожу к следующему
            if subject is None or not subject.lower().startswith('жалоба'):
                continue
            else:
                # Обрезаю слева слово жалоба и символы пунктуации с пробелами
                subject = subject.lower().lstrip('жалоба' + string.whitespace + string.punctuation)
                subject = subject.capitalize()

            # Достаю адрес почты автора. Не проверяю на None предполагая, что From всегда указан
            email_author = decode_header(message['From'])[1][0].decode()

            # Достаю текст письма
            text = ''
            for part in message.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    text += b64decode(part.get_payload()).decode().strip()

            email_schema = CreateTaskFromEmailS(
                title=subject or 'Тема не указана.',
                description=text,
                status=Status.open,
                project_id=settings.MAIL_PROJECT_ID,
                author_id=settings.BOT_USER_ID,
                email_uid=uid,
                email_author=email_author,
            )
            emails.append(email_schema)

        return emails
