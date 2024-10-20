from abc import ABC, abstractmethod

class BaseDestination(ABC):
    @abstractmethod
    def connect(self):
        """Connect to the destination database."""
        pass

    @abstractmethod
    def insert_data(self, data):
        """Insert data into the destination database."""
        pass
