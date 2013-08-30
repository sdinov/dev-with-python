import socket
import threading
import time
import select
import errno

class ClientSocket:
    address = ""
    port = ""
    my_socket = None
    BUFF_SIZE = 4096
    select_timeout = 5
    running = False
    thread = None
    
    def __init__(self, address, port):
        self.address = address
        self.port = port
            
    def connect(self):
        result = "Connected to {}:{}".format(self.address, self.port)
        if self.address == "" or self.port == "" or self.port == 0 or self.address == 0:
            return "Can not connect due to invalid input arguments"
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.my_socket.connect((self.address, self.port))
            self.thread = threading.Thread(target=self.select_thread)
            self.thread.start()
            #self.thread.join()
            sockname = self.my_socket.getsockname()
            peername = self.my_socket.getpeername()
            result = (sockname, peername)
        except Exception as data:
            print("Failed to connect to {}:{} because {}".format(self.address, self.port, data))
            return
        print("Connected to {}:{}".format(result[0][0], result[0][1]))
        return result

    def close(self):
        result = "Closed connection to {}:{}".format(self.address, self.port)
        if self.my_socket is not None:
            try:
                self.my_socket.close()
            except Exception as data:
                result = "Failed to close the socket because {}".format(data)
        else:
            return "Trying to close a None socket"
        self.my_socket = None
        return result

    def send(self, data):
        total_sent_bytes = 0
        if self.my_socket is not None:
            try:
                while total_sent_bytes < len(data):
                    sent_bytes = self.my_socket.send(bytes(data[total_sent_bytes:],'UTF-8'))
                    total_sent_bytes = total_sent_bytes + sent_bytes;
            except Exception as exception_msg:
                print("Couldn't sent bytes because of {}".format(exception_msg))
                return
        else:
            return "Can not send - socket is closed"
        return "Sent {} bytes of data".format(total_sent_bytes)

    def receive(self, data_buffer):
        if self.my_socket is not None:
            try:
                data_buffer = self.my_socket.recv(self.BUFF_SIZE)
                if len(data_buffer) == 0:
                    print("Connection with {}:{} was broken, closing socket"\
                    .format(self.address, self.port))
                    self.close()
                    self.running = False
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    print(err)
                    return
                else:
                    return "Couldn't receive data because {}".format(e)
        else:
            return "The socket is not connected to {}:{}".format(self.address, self.port)

        return "Received {} bytes of data".format(len(data_buffer))

    def select_thread(self):
        self.running = True
        self.my_socket.setblocking(0)
        print("Started select thread...")
        while self.running is True and self.my_socket is not None:
            ready_readers, ready_writers, ready_errors =\
            select.select([self.my_socket], [self.my_socket], [self.my_socket], self.select_timeout)
            if ready_readers != []:
                msg = ''
                res = self.receive(msg)
                print(res);
            if ready_errors != []:
                print("Error on the socket: {}".format(errno))
                self.my_socket.close()
                self.running = False
            if ready_writers != []:
                #self.send("\r\n")
                time.sleep(1)
                
    def stop(self):
        print("Stopping the socket...")
        self.running = False
        time.sleep(self.select_timeout)
