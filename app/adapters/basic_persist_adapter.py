from abc import ABC, abstractmethod
import logging


class BasicPersistAdapter(ABC):
    def __init__(self, adapterd_class, logger=None):
        self._class = adapterd_class
        self._logger = logger if logger else logging.getLogger()

    @property
    def logger(self):
        return self._logger

    @property
    def adapter_class(self):
        return self._class

    @property
    def adapted_class_name(self):
        return self._class.__name__

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, serialized_data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id):
        raise NotImplementedError

    @abstractmethod
    def filter(self, **kwargs):
        raise NotImplementedError
