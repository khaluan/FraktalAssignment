from client.protocol.interface import Client
import requests

class HTTPSClient(Client):
    def __init__(self, ip: str, port: int):
        self.connect(ip, port)

    def connect(self, ip: str, port: int) -> None:
        self.url = f'https://{ip}:{port}/' 

    def send_file(self, filename: str) -> None:
        response = requests.post(self.url, files={filename: open(filename, 'rb')}, verify=False)
        # print(response)

    def send(self, payload: str | bytes) -> None:
        response = requests.post(self.url, data=payload, verify=False)
        # print(response)

    def name(self) -> str:
        return "HTTPS"