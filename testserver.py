from UDPR import serverSockRef

server = serverSockRef(("127.0.0.1", 5024), 1024)
while True:
    print(server.recv_data())