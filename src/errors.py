class AppError(Exception):
    message: str

    def __init__(self):
        super().__init__(self.message)


class AlreadyExistsError(AppError):
    def __init__(self, what: str):
        self.message = f'{what} is already exist.'
        super().__init__()


class WasNotFoundError(AppError):
    def __init__(self, what: str):
        self.message = f'{what} was not found.'
        super().__init__()


class InvalidEmailOrPasswordError(AppError):
    def __init__(self):
        self.message = 'Invalid email or password.'
        super().__init__()


