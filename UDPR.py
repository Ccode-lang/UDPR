from socket import *
import hashlib
import json

class clientSockRef:
    def __init__(self, sock : socket, sendIP):
        self.sock = sock
        self.sendIP = sendIP
        
    def send_data(self, data : str):
        message_meta = {
            data : hashlib.md5(data.encode()).hexdigest()
        }
        self.sock.sendto(json.dumps(message_meta).encode(), self.sendIP)

        message, client_address = self.sock.recvfrom(20)

        valid = message.decode() == "VALID"

        while not valid:
            print("Message was invalid resending")
            #message_meta[list(message_meta.keys())[0]] = hashlib.md5(data.encode()).hexdigest()
            self.sock.sendto(json.dumps(message_meta).encode(), self.sendIP)
            message, client_address = self.sock.recvfrom(20)
            valid = message.decode() == "VALID"

class serverSockRef:
    def __init__(self, IP : tuple, bufsize : int):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(IP)
        self.IP = IP
        self.bufsize = bufsize
        
    def recv_data(self):
        message, client_address = self.sock.recvfrom(self.bufsize)

        message_meta: dict = json.loads(message)
        message_data = list(message_meta.keys())[0]
        message_checksum = message_meta[message_data]
        while hashlib.md5(message_data.encode()).hexdigest() != message_checksum:
            self.sock.sendto(b"INVALID", client_address)
            print("invalid")

            message, client_address = self.sock.recvfrom(self.bufsize)
            message_meta = json.loads(message)
            message_data = list(message_meta.keys())[0]
            message_checksum = message_meta[message_data]
        
        self.sock.sendto(b"VALID", client_address)

        return message_data