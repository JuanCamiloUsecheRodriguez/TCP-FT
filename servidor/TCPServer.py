import socket, threading, os, hashlib, sys
from time import sleep


host, port = '', 9000
SIZE = 32000
hasher = hashlib.md5()




class transfer :

    socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        numCli = int(sys.argv[1])
        file_name = sys.argv[2]
        self.socketServidor.bind((host, port))
        print(' Server is ready ..')
        self.socketServidor.listen(5)
        threads = []
        idCli =1
        while numCli >0:
            conn, addr = self.socketServidor.accept()
            size = os.path.getsize(file_name)
            print(' file size : {}'.format(str(size)))
            send_thread = threading.Thread(target = self.send_file, args=(file_name, size, conn, addr, idCli ))
            threads.append(send_thread)
            numCli = numCli - 1
            idCli=idCli+1
        for thread in threads:
            thread.start()

    def send_file(self, file_name, size, conn, addr, idCli):
        size = os.path.getsize(file_name)
        conn.send(file_name.encode('utf-8'))
        conn.send(str(size).encode('utf-8'))
        conn.send(str(idCli).encode('utf-8'))
        i = 0
        bytesSent = 0
        print(' file size : {}'.format(str(size)))
        with open(file_name, 'rb') as file:
            data = file.read(SIZE)
            conn.send(data)
            while data != bytes(''.encode()):
                #print(data)
                data = file.read(SIZE)
                sent = conn.send(data)
                i = i+1
                bytesSent = bytesSent+sent
                if sent != SIZE:
                    sent = conn.send(b'Fin')
                    print('Fin')
                    break
            conn.send(str(bytesSent).encode('utf-8'))
            sleep(0.5)
            conn.send(str(i).encode('utf-8'))
            buf = file.read()
            hasher.update(buf)
            hash_servidor = hasher.hexdigest()
            conn.send(str(hash_servidor).encode('utf-8'))





Transfer = transfer()