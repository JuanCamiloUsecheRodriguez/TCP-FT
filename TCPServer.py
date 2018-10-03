import socket, threading, os
from time import sleep


host, port = '', 9000


class transfer :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        self.mysocket.bind((host, port))
        print(' Server is ready ..')
        self.mysocket.listen(5)
        while True:
            conn, addr = self.mysocket.accept()

            file_name = '4k.jpg'
            size = os.path.getsize(file_name)
            print(' file size : {}'.format(str(size)))
            send_thread = threading.Thread(target = self.send_file, args=(file_name, size, conn, addr, ))
            send_thread.start()

    def send_file(self, file_name, size, conn, addr):
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            conn.send(data)
            while data != bytes(''.encode()):
                #print(data)
                data = file.read(1024)
                conn.send(data)

            print(' File sent successfully.')


Transfer = transfer()