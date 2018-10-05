
import socket, sys, threading, hashlib,time, logging,os
from time import gmtime, strftime
from time import sleep
from sys import stderr
from logging import getLogger, StreamHandler, Formatter, DEBUG

host, port = '', 9000
TAMANO = 2048
hasher = hashlib.md5()
tamano = 0

class transfer :

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        numCli = int(sys.argv[1])
        file_name = sys.argv[2]
        self.serversocket.bind((host, port))
        print(' Server ready for connections')
        self.serversocket.listen(5)
        threads = []
        id_cliente =1
        while numCli >0:
            tamano = os.path.getsize(file_name)
            conn, addr = self.serversocket.accept()
            print(' file TAMANO : {}'.format(str(TAMANO)))
            send_thread = threading.Thread(target = self.send_file, args=(file_name, tamano, conn, id_cliente ))
            threads.append(send_thread)
            numCli = numCli - 1
            id_cliente=id_cliente+1
        for thread in threads:
            thread.start()

    def send_file(self, file_name, tamano, conn, id_cliente):

        l = getLogger()
        os.makedirs(os.path.dirname('./logs/TCP{}.log'.format(id_cliente)), exist_ok=True)
        logging.basicConfig(format='%(message)s', filename='./logs/TCP{}.log'.format(id_cliente), level=logging.DEBUG)
        sh = StreamHandler(stderr)
        sh.setLevel(DEBUG)
        f = Formatter(' %(message)s')
        sh.setFormatter(f)
        l.addHandler(sh)
        l.setLevel(DEBUG)
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        l.info('%s#%s', 'FECHA', showtime)
        l.info('%s#%s', 'NOMBRE_ARCHIVO', file_name)
        l.info('%s#%s', 'TAMANO_ARCHIVO', tamano)
        l.info('%s#%s', 'ID_CLIENTE', id_cliente)
        i = 0
        bytesSent = 0
        with open(file_name, 'rb') as file:
            tamano = os.path.getsize(file_name)
            data = file.read(TAMANO)
            start_time = time.time()
            conn.send(data)
            while data != bytes(''.encode()):
                data = file.read(TAMANO)
                sent = conn.send(data)
                i = i+1
                print(len(data))
                bytesSent = bytesSent+sent
                if sent < TAMANO:
                    sent = conn.send(b'Fin')
                    print('Fin')
                    break

            elapsed_time = time.time() - start_time
            print(' File sent successfully.')
            l.info('FILE_DELIVERY;SUCCESS')
            l.info('%s#%s', 'BYTES_ENVIADOS', bytesSent)
            l.info('%s#%s', 'BYTES_RECIBIDOS', bytesSent)
            l.info('%s#%s', 'PAQUETES_ENVIADOS', i)
            l.info('%s#%s', 'PAQUETES_RECIBIDOS', i)
            l.info('%s#%s', 'TIEMPO_TOTAL', elapsed_time)
            l.info('-----------------------------------')





Transfer = transfer()