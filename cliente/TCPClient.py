import socket, sys, hashlib

#USAR ESTO PARA ALTERNAR LAS PRUEBAS ENTRE LOCAL Y REMOTO
host, port = '157.253.205.19', 9000
#host, port = 'localhost', 9000
hasher = hashlib.md5()
SIZE=60000

class recv_data :

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientsocket.connect((host, port))
    def __init__(self):
        print('Connected successfully')
        data = self.clientsocket.recv(SIZE)
        i=0
        bytesReceived=0
        #EL CLIENTE EMPEZARA A ESCRIBIR LO QUE RECIBE EN UN destiny_file
        with open(sys.argv[1], 'wb+') as destiny_file:
            while data != bytes(''.encode()):
                destiny_file.write(data)
                data = self.clientsocket.recv(SIZE)
                bytesReceived=bytesReceived+len(data);
                i=i+1
                if data == b'Fin' :
                    break
            buf = destiny_file.read()
            hasher.update(buf)
            hash_cliente = hasher.hexdigest()
            print('DONE')



re = recv_data()