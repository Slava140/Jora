
class AlreadyExistsError(Exception):
    def __init__(self, what: str):
        super().__init__(f'{what} is already exist.')


class WasNotFoundError(Exception):
    def __init__(self, what: str):
        super().__init__(f'{what} was not found.')


class InvalidEmailOrPasswordError(Exception):
    def __init__(self):
        super().__init__('Invalid email or password.')
