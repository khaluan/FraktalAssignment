# Fraktal Project

This repository contains the code for the Fraktal project, which includes both client and server applications. The client application can send messages or files using different protocols (HTTPS, DNS, SMTP), and the server application can receive and process these messages or files.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Docker](#docker)
- [Kubernetes](#kubernetes)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker
- Docker Compose

### Clone the Repository

```sh
git clone https://github.com/khaluan/FraktalAssignment.git
cd FraktalAssginment
```

### Install Python Dependencies
```sh
pip install -r requirements.txt
```
## Usage
### Client Application
The client application can send messages or files using different protocols. You can specify which clients to include, which message to send, or which file to send via command-line arguments.

```sh
python -m client.main --clients https dns --message "Hello, world!"  --size 1000 --rate 5
python -m client.main --clients smtp --file "/etc/passwd"
```

The client application is based on a manager that could change to a different protocol when the current protocol is blocked. 

### Server Application
The server application can receive and process messages or files sent by the client application. User could select to deploy all or few selective protocols on this server.

```sh
python -m server.main 
```

### Environment variables
The environment variables are stored in the corresponding **[server/client]/config.py** and the credential should be setup in the **.env** file

One important notice is that it is recommended to use two different accounts when exfiltrating data with SMTP, since the credential of the sender is deployed into the victim environment, therefore, that mailbox is considered to be fully compromised. Hence it is not recommended to store any information in that mailbox. All the sent email will be removed immediately.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Technical details
The application tries to send data using different protocol by abusing different fields of the network packet based on the corresponding protocols.

### HTTPS
HTTPS provides a secure communication with TLS. Therefore, it is straightforward to put the data into the body of the requests. In this project, the server setup a simple HTTPS server handle the POST requests. 

The body of the request is used to store data. In case of sending a file, it is encoded using multi-part form. In this case the communication don't need any further encryption since the traffic is already protected with TLS. 

Further protection could be employed encrypt the SNI using the ECH extension in TLS 1.3 to further hide the traffic among benign TLS traffics. However, this is not implemented in this project due to time constraint.

### DNS
DNS is a protocol used to translate human readable names to IP addresses. DNS is based on UDP, and is widely used without encryption. Therefore, the content of the traffic could be analyzed with intrusion detection systems. Therefore, to make it unreadable by the IDS, we need to perform an encryption step before sending the message. 

The client will initiate a request for A record of the specific domain to the server with a specific name to get the encryption key. The key will be in base64 encoding stored in the domain name of the response. Since the encryption key is small it could easily fit into the domain name. 

Then all the subsequent traffic will encrypt the message that needs to be sent, and stored it in an additional TXT record. Since the TXT records allow up to 255 bytes of additional data, it could be abused to encode the data.

However, the DNS requests and response is limited in terms of throughput, it is only effective to extract small data or message. If the size of the data is large, it would result in either big DNS request, or high number of requests per second. Due to this nature, the DNS client only support sending message instead of files.

### SMTP
We use SMTP to create an email from sender to the receiver with the data attached to the body and the extracted files as the attachment. We abuse the smtp server of Google to create a higher credability since it has good reputation and is not likely to be blocked by IDS.

The server just simple check for any new message after a period of time, parse the data and the attachment in the email. However, each attachment is only limited up to 25MB by Google mail service. For a large file exfiltration, the client could split the file into 25MB chunks and send it over the SMTP with the order embedded in the filename.  Then the server can parse that data and reconstruct the file based on the order. The feature is possible to implement, however, due to the time constraint, the implementation is not included in this projects. The client in this projects only support files that is less than 25MB.

### Traffic controllers
We provides 2 types of traffic controllers, including the packet size controller and the time controller. This is inspired by the common behavior of the IDS, which is detecting the data exfiltration based on large traffic to a destination server or high number of traffic during a period of time.

#### Package size controller
This controller will try to split the message into smaller chunks with variable length to make the traffic looks the same as the normal traffic. The controller can be configure to have the average payload length for each requests.

This can be set at client with --size [size] flag and only available for sending message

#### Time-based controller
The controller creates pauses between different requests to reduce the high volumn of connection between the client and the server. This controller can be configured by specifying the maximum number of connection per seconds

This can be set at client with --rate [rate] flag and only available for sending message