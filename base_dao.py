from abc import ABC, abstractmethod


class BaseDAO(ABC):
    model = None

    @abstractmethod
    def select_one_or_none(self):
        pass

    @abstractmethod
    def select_all_or_none(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
