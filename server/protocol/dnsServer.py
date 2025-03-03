from dnslib.server import DNSServer, BaseResolver, DNSLogger
from dnslib import RR, QTYPE, A
from multiprocessing import Process, Queue
from base64 import b64encode

from utils.crypto import generate_key, decrypt
from server.config import *
from server.protocol.interface import ServerLauncher, Server

class DnsServer(Server):
    def __init__(self, txt_queue: Queue):
        self.txt_queue = txt_queue
        self.ip = DNS_SERVER_IP
        self.port = DNS_PORT

    class LocalhostResolver(BaseResolver):
        def __init__(self, txt_queue: Queue):
            self.txt_queue = txt_queue
            self.key = ''

        def resolve(self, request, handler):
            reply = request.reply()
            qname = request.q.qname
            qtype = QTYPE[request.q.qtype]
            
            if qtype == 'A':
                if qname == DOMAIN_NAME:
                    self.key = generate_key()
                    reply.add_answer(RR(b64encode(self.key), QTYPE.A, rdata=A('127.0.0.1'), ttl=60))
                else:
                    for additional_record in request.ar:
                        self.txt_queue.put(decrypt(additional_record.rdata.data[0], self.key).decode())
            else:
                reply.header.rcode = 3  # NXDOMAIN
            
            return reply

    def run(self):
        resolver = self.LocalhostResolver(self.txt_queue)
        logger = DNSLogger("error", False)
        server = DNSServer(resolver, address=DNS_SERVER_IP, port=DNS_PORT, logger=logger)
        server.start()

class DNSServerLauncher(ServerLauncher):
    def __init__(self, txt_queue: Queue):
        self.txt_queue = txt_queue
        self.ip = DNS_SERVER_IP
        self.port = DNS_PORT
        self.process = None

    def launch(self):
        server = DnsServer(self.txt_queue)
        self.process = Process(target=server.run)
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.join()