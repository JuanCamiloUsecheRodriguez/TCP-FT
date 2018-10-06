
import socket, sys, threading, hashlib,time, logging,os
from sys import stderr
from time import gmtime, strftime
from logging import getLogger, StreamHandler, Formatter, DEBUG
#ESTAS SIMPLEMENTE SON VARIABLES
host, port = '', 9000
hasher = hashlib.md5()
TAMANO = 2048
tamano = 0

class transfer :
    #ESTE ES EL SOCKET QUE VAMOS  USAR
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        numCli = int(sys.argv[1])
        file_name = sys.argv[2]
        self.serversocket.bind((host, port))

        print('Ready to receive connections')
        self.serversocket.listen(5)
        id_cliente = 1
        threads = []

        #VAMOS A ESPERAR A QUE SE CONECTEN TODOS LOS CLIENTES ANTES DE INICIAR LOS THREADS QUE TRANSFIEREN EL ARCHIVO A CADA UNO
        while numCli > 0 :
            tamano = os.path.getsize(file_name)
            conn, addr = self.serversocket.accept()
            send_thread = threading.Thread(target = self.send_file, args=(file_name, tamano, conn, id_cliente ))
            threads.append(send_thread)
            numCli = numCli - 1
            id_cliente=id_cliente+1
        for thread in threads:
            thread.start()

    #AQUI INICIA    N LOS THREADS
    def send_file(self, file_name, tamano, conn, id_cliente):

        logger = getLogger()
        os.makedirs(os.path.dirname('./logs/TCP{}.log'.format(id_cliente)), exist_ok=True)
        logging.basicConfig(format='%(message)s', filename='./logs/TCP{}.log'.format(id_cliente), level=logging.DEBUG)
        sh = StreamHandler(stderr)
        sh.setLevel(DEBUG)
        f = Formatter(' %(message)s')
        sh.setFormatter(f)
        logger.addHandler(sh)
        logger.setLevel(DEBUG)
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logger.info('%s#%s', 'FECHA', showtime)
        logger.info('%s#%s', 'NOMBRE_ARCHIVO', file_name)
        logger.info('%s#%s', 'TAMANO_ARCHIVO', tamano)
        logger.info('%s#%s', 'ID_CLIENTE', id_cliente)
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
            logger.info('ENVIO_DEL_ARCHIVO#EXITOSO')
            logger.info('%s#%s', 'BYTES_ENVIADOS', bytesSent)
            logger.info('%s#%s', 'BYTES_RECIBIDOS', bytesSent)
            logger.info('%s#%s', 'PAQUETES_ENVIADOS', i)
            logger.info('%s#%s', 'PAQUETES_RECIBIDOS', i)
            logger.info('%s#%s', 'TIEMPO_TOTAL', elapsed_time)
            logger.info('----------------------------')

Transfer = transfer()