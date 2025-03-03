from abc import ABC, abstractmethod
class Server(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

class ServerLauncher(ABC):
    @abstractmethod
    def launch(self) -> None:
        pass

    def stop(self) -> None:
        if self.process:
            self.process.terminate()
            self.process.join()
