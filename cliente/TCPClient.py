import socket, sys, threading, hashlib,time, logging,os


host, port = '157.253.205.19', 9000
#host, port = 'localhost', 9000
hasher = hashlib.md5()
SIZE=2048

class recv_data :
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientsocket.connect((host, port))
    def __init__(self):
        print('Connected successfully')
        data = self.clientsocket.recv(SIZE)
        i=0
        bytesReceived=0
        with open(sys.argv[1], 'wb+') as f:
            while data != bytes(''.encode()):
                f.write(data)
                data = self.clientsocket.recv(SIZE)
                bytesReceived=bytesReceived+len(data);
                i=i+1
                if data == b'Fin' :
                    print('Fin de archivo')
                    break

            buf = f.read()
            hasher.update(buf)
            hash_cliente = hasher.hexdigest()
            print('hash: ', hash_cliente)
            print('termino')



re = recv_data()