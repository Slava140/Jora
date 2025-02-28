import logging

from flask import has_request_context, request

from config import settings

logs_dir = settings.SRC_PATH.parent / 'logs'
logs_dir.mkdir(exist_ok=True)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.remote_addr = ''
        record.method = ''
        record.url = ''
        if has_request_context():
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.url = request.url
        return super().format(record)


config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'class': 'logger_config.RequestFormatter',
            'format': '{asctime} {levelname:^9} '
                      '{remote_addr:^15} {method:^7} {url}: {message}',
            'style': '{',
        },
        'detailed': {
            'class': 'logger_config.RequestFormatter',
            'format': '{asctime} {levelname:^9} [{filename:>15}:{lineno:<4}] '
                      '{remote_addr:^15} {method:^7} {url}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'filename': logs_dir / 'app.log',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'werkzeug': {
            'level': 'WARNING'
        },
        'sqlalchemy.engine': {
            'level': 'WARNING'
        }
    },
}
