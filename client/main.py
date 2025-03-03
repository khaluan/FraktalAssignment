import argparse

from client.manager import ProtocolManager
from client.protocol.dnsClient import DNSClient
from client.protocol.httpsClient import HTTPSClient
from client.protocol.smtpClient import SMTPClient    
from client.config import *
from controllers.rateController import TimeBaseController, RandomBalanceRateController


def parse_args():
    parser = argparse.ArgumentParser(description="Client application to send messages or files using different protocols.")
    parser.add_argument('--clients', nargs='+', choices=['https', 'dns', 'smtp'], required=True, help="List of clients to include (https, dns, smtp)")
    parser.add_argument('--message', type=str, help="Message to send")
    parser.add_argument('--file', type=str, help="File to send")
    parser.add_argument('--rate', type=float, help="Rate of sending messages/files")
    parser.add_argument('--size', type=int, help="Size of the payload per connection")
    return parser.parse_args()

if __name__ == "__main__":
    manager = ProtocolManager(max_retries=3)
    
    args = parse_args()
    # Register clients
    if 'https' in args.clients:
        manager.register_client(client=HTTPSClient(SERVER_IP, HTTPS_PORT))
    if 'dns' in args.clients:
        manager.register_client(client=DNSClient(DNS_SERVER_IP, DNS_PORT, DOMAIN_NAME))
    if 'smtp' in args.clients:
        manager.register_client(client=SMTPClient(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL))
    
    if args.rate:
        manager.register_time_controller(TimeBaseController(max_connections=args.rate))
    if args.size:
        manager.register_size_controller(RandomBalanceRateController(avg_rate=args.size))


    if args.message:
        manager.send(args.message)
    if args.file:
        manager.send_file(args.file)    