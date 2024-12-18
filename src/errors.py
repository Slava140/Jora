class AppError(Exception):
    def __init__(self, message: str = 'Unknown error.', status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AlreadyExistsError(AppError):
    def __init__(self, what: str | None = None):
        message = f'{what} is already exist' if what is not None else 'Already exist.'
        super().__init__(message=message, status_code=409)


class WasNotFoundError(AppError):
    def __init__(self, what: str | None = None):
        message = f'{what} was not found.' if what is not None else 'Not Found.'
        super().__init__(message=message, status_code=404)


class InvalidEmailOrPasswordError(AppError):
    def __init__(self):
        super().__init__(message='Invalid email or password.', status_code=401)


class MustBePositiveError(AppError):
    def __init__(self, what: str | None = None):
        message = f'{what} must be positive.' if what is not None else 'Must be positive.'
        super().__init__(message=message, status_code=400)


class ExtensionsNotAllowedError(AppError):
    def __init__(self, what: str | None = None):
        message = f'File extension "{what}" is not allowed.' if what is not None else 'File extension is not allowed.'
        super().__init__(message=message, status_code=415)


class FileIsNotAttachedError(AppError):
    def __init__(self):
        message = 'File is not attached'
        super().__init__(message=message, status_code=400)
