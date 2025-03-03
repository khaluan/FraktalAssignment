from abc import ABC, abstractmethod
class Client(ABC):
    @abstractmethod
    def send(self, payload: str | bytes) -> None:
        pass

    @abstractmethod
    def send_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
