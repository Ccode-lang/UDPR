from UDPR import clientSockRef
from socket import *

client = clientSockRef(socket(AF_INET, SOCK_DGRAM), ("127.0.0.1", 5024))
num = 0
while True:
    num += 1
    client.send_data(str(num))