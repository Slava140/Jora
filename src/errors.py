
class AlreadyExistsError(Exception):
    def __init__(self, what: str):
        super().__init__(f'{what} is already exist.')
