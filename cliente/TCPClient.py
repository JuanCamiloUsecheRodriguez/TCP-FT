import socket, sys, threading, hashlib,time, logging,os
from time import gmtime, strftime

from sys import stderr
from logging import getLogger, StreamHandler, Formatter, DEBUG
from time import sleep

#configuracion del logger
l = getLogger()
os.makedirs(os.path.dirname('./logs/TCP.log'), exist_ok=True)
logging.basicConfig(format='%(message)s', filename='./logs/TCP.log',  level=logging.DEBUG)
sh = StreamHandler(stderr)
sh.setLevel(DEBUG)
f = Formatter(' %(message)s')
sh.setFormatter(f)
l.addHandler(sh)
l.setLevel(DEBUG)


host, port = 'localhost', 9000
hasher = hashlib.md5()
SIZE=32000

showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
l.info('%s#%s','FECHA',showtime)


class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))
    def __init__(self):
        print('Connected successfully')
        start_time = time.time()
        filename = self.mysocket.recv(SIZE)
        filesize = self.mysocket.recv(SIZE)
        idCliente = self.mysocket.recv(SIZE)
        data = self.mysocket.recv(SIZE)
        i=0
        bytesReceived=0
        f = open(filename.decode('utf-8'), 'wb+')
        while data != bytes(''.encode()):
            #print(data)
            f.write(data)
            data = self.mysocket.recv(SIZE)
            bytesReceived=bytesReceived+len(data);
            i=i+1
            if data == b'Fin' :

                break
        buf = f.read()
        hasher.update(buf)
        hash_cliente = hasher.hexdigest()

        print('hash: ', hasher.hexdigest())



        l.info('%s#%s', 'NOMBRE_ARCHIVO', filename.decode('utf-8'))
        l.info('%s#%s', 'TAMANO_ARCHIVO', filesize.decode('utf-8'))
        l.info('%s#%s', 'ID_CLIENTE', idCliente.decode('utf-8'))

        bytesSent = self.mysocket.recv(SIZE)
        numPack = self.mysocket.recv(SIZE)

        hash_servidor = self.mysocket.recv(SIZE)
        hash_servidor = hash_servidor.decode('utf-8')
        if hash_servidor == hash_cliente:
            l.info('ENVIO_ARCHIVO#EXITOSO')

        else:
            l.info('ENVIO_ARCHIVO#FALLO')

        l.info('%s#%s', 'BYTES_ENVIADOS', bytesSent.decode('utf-8'))
        l.info('%s#%s', 'BYTES_RECIBIDOS', str(bytesReceived-3))

        elapsed_time = time.time() - start_time
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print('TIME ELAPSED: ', elapsed_time)
        l.info('%s#%s', 'PAQUETES_ENVIADOS', numPack.decode('utf-8'))
        l.info('%s#%s', 'PAQUETES_RECIBIDOS', i-1)

        l.info('%s#%s', 'TIEMPO_TOTAL', elapsed_time)
        l.info('------------------------------')
        logging.shutdown()
        os.rename('./logs/TCP.log', './logs/TCP{}.log'.format(idCliente.decode('utf-8')))




re = recv_data()