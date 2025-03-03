from server.manager import ServerManager
from server.protocol.httpsServer import HttpsServerLauncher
from server.protocol.dnsServer import DNSServerLauncher
from server.protocol.smtpServer import SMTPServerLauncher
from server.config import *

if __name__ == "__main__":
    manager = ServerManager()
    
    # Register servers
    manager.register_server(HttpsServerLauncher(manager.txt_queue, manager.file_queue))
    manager.register_server(DNSServerLauncher(manager.txt_queue))
    manager.register_server(SMTPServerLauncher(manager.txt_queue, manager.file_queue))

    try:
        while True:
            # Receive data
            data = manager.recv()
            filenames = manager.get_file()
            if data:
                with open('received.txt', 'a') as f:
                    f.write(data)
            if filenames:
                print(f'File received: {filenames}')
    except KeyboardInterrupt:
        manager.stop_servers()