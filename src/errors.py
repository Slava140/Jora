class AppError(Exception):
    def __init__(self, message: str = 'Unknown error.', status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AlreadyExistsError(AppError):
    def __init__(self, what: str):
        super().__init__(message=f'{what} is already exist.', status_code=409)


class WasNotFoundError(AppError):
    def __init__(self, what: str):
        super().__init__(message=f'{what} was not found.', status_code=404)


class InvalidEmailOrPasswordError(AppError):
    def __init__(self):
        super().__init__(message='Invalid email or password.', status_code=401)


