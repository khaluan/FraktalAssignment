from client.protocol.interface import Client
from controllers.rateController import NormalSizeRateController, NormalTimeRateController
from controllers.interface import SizeRateController, TimeRateController
import random 
import time

class ProtocolManager:
    def __init__(self, max_retries: int = 3, time_controller: TimeRateController = NormalTimeRateController(), size_controller: SizeRateController = NormalSizeRateController()):
        self.clients = []
        self.blocked_clients = []
        self.max_retries = max_retries
        self.time_controller = time_controller
        self.size_controller = size_controller

    def register_time_controller(self, controller: TimeRateController) -> None:
        self.time_controller = controller

    def register_size_controller(self, controller: SizeRateController) -> None:
        self.size_controller = controller

    def register_client(self, client: Client) -> None:
        self.clients.append(client)


    def send(self, payload: bytes | str) -> None:
        chunks = self.size_controller.dissect(payload)
        breaks = self.time_controller.get_pauses(len(chunks))
        print(chunks)
        for i in range(len(chunks)):
            self.send_chunk(chunks[i])
            if i < len(breaks):
                time.sleep(breaks[i])

    def send_chunk(self, chunk: bytes | str) -> object:
        retries = 0
        while retries < self.max_retries:
            index = random.randint(0, len(self.clients) - 1)
            client = self.clients[0]
            try:
                result = client.send(chunk)
                return result
            except Exception as e:
                print(f"Send error with client {client.name()}: {e}")
                retries += 1
                if retries >= self.max_retries:
                    self.blocked_clients.append(client)
                    self.clients.pop(0)
                    retries = 0
                    if not self.clients:
                        raise Exception("All protocols failed to send the payload and are blocked")
        raise Exception("All protocols failed to send the payload")

    def send_file(self, filepath: str) -> object:
        retries = 0
        while retries < self.max_retries:
            index = random.randint(0, len(self.clients) - 1)
            client = self.clients[0]
            try:
                result = client.send_file(filepath)
                return result
            except Exception as e:
                print(f"Send error with client {client.name()}: {e}")
                retries += 1
                if retries >= self.max_retries:
                    self.blocked_clients.append(client)
                    self.clients.pop(0)
                    retries = 0
                    if not self.clients:
                        raise Exception("All protocols failed to send the payload and are blocked")
        raise Exception("All protocols failed to send the payload")
