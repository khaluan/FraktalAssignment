import socket
from dnslib import DNSRecord, QTYPE, RR, TXT
from client.config import *
from base64 import b64decode
from utils.crypto import encrypt
from client.protocol.interface import Client
from typing import Generator

class DNSClient(Client):
    def __init__(self, dns_server_ip: str, dns_port: int, domain: str):
        self.dns_server = dns_server_ip
        self.port = dns_port
        self.domain = domain
        self.get_key()

    def chunk_payload(self, payload: str | bytes, chunk_size: int = 150) -> Generator[str, None, None]:
        for i in range(0, len(payload), chunk_size):
            yield payload[i:i + chunk_size]

    def get_key(self) -> None:
        # Create a DNS request for the A record of the domain 'localhost'
        qname = DOMAIN_NAME
        qtype = "A"
        request = DNSRecord.question(qname, qtype)

        # Convert the DNS request to bytes
        data = request.pack()

        # Create a UDP socket connection to localhost on port 5353
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, (self.dns_server, self.port))

            # Receive response
            response_data, _ = s.recvfrom(1024)
            response = DNSRecord.parse(response_data)
            # print(f"Received response: {response}")

            # Extract the key from the response
            key = response.rr[0]._rname.label[0]
            self.key = b64decode(key)
            

    def send(self, payload: str | bytes) -> None:
        # Create a DNS request for the TXT record of the domain 'localhost'
        qname = "sub.mydomain.com"
        qtype = "A"
        request = DNSRecord.question(qname, qtype)
        for text in self.chunk_payload(payload):
            request.add_ar(RR(qname, QTYPE.TXT, rdata=TXT(encrypt(text.encode(), self.key)), ttl=60))

        # Convert the DNS request to bytes
        data = request.pack()

        # Create a UDP socket connection to localhost on port 5353
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, (self.dns_server, self.port))

    def send_file(self, filename):
        pass

    def name(self) -> str:
        return "DNS"
