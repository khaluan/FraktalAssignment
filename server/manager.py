from multiprocessing import Queue
from server.protocol.interface import ServerLauncher

class ServerManager:
    def __init__(self):
        self.servers = []
        self.files = []
        self.txt_queue = Queue()
        self.file_queue = Queue()
        self.txt_buffer = ''

    def register_server(self, launcher: ServerLauncher) -> None:
        """
        Register a server to the server manager, so that the manager can flexibly switch between different servers.
        
        Args:
            ip (str): The IP address of the server.
            port (int): The port number of the server.
        """
        self.servers.append(launcher)
        launcher.launch()

    def recv(self) -> None:
        """
        Retrieve data from the queue.
        
        Returns:
            bytes: The received data.
        """
        while not self.txt_queue.empty():
            data = self.txt_queue.get()
            self.txt_buffer += data

        text = self.txt_buffer
        self.txt_buffer = ''
        return text
        
    def get_file(self):
        new_filenames = []
        
        while not self.file_queue.empty():
            data = self.file_queue.get()
            filename, content = data
            new_filenames.append(filename)
            filename = filename.replace('/', '_')
            with open(f'./files/{filename}', 'wb+') as f:
                f.write(content)

        return new_filenames


    
    def stop_servers(self) -> None:
        """
        Stop all registered servers.
        """
        for server in self.servers:
            server.stop()

