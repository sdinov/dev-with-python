import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from client_socket import *
import unittest

class TestSocketFunctions(unittest.TestCase):

    def setUp(self):
        self.client_socket = ClientSocket("10.255.4.7", 5060)

    def test_connect_success(self):
        # test if connect is successful
        self.assertNotEqual(self.client_socket.connect(), "Not connected")
        self.client_socket.stop()
        self.client_socket.close()

    def test_connect_fail(self):
        # test if connect will fail if address,port are not correct
        self.client_socket.set_address("127.0.0.1")
        self.client_socket.set_port("5060")
        self.assertEqual(self.client_socket.connect(), "Not connected")
        self.client_socket.stop()
        self.client_socket.close()

    def test_send_no_connect(self):
        # test send must fail if the socket is not connected
        self.assertEqual(self.client_socket.send("alabala"),\
                         "Can not send - socket is closed")
        self.client_socket.stop()
        self.client_socket.close()

    def test_send(self):
        # test send must succeed if the socket is connected
        self.client_socket.connect()
        self.assertNotEqual(self.client_socket.send("alabala"),\
                         "Can not send - due to exception" or \
                         "Can not send - socket is closed")
        self.client_socket.stop()
        self.client_socket.close()
        
    def test_receive_no_connect(self):
        # test receive must fail if the socket is not connected
        msg = ''
        self.assertEqual(self.client_socket.receive(msg),\
                         "The socket is not connected.")
        self.client_socket.stop()
        self.client_socket.close()
    
    def test_receive(self):
        # test receive must return EAGAIN or EWOULDBLOCK if called when no
        # bytes are available for reading
        self.client_socket.connect()
        msg = ''
        self.assertEqual(self.client_socket.receive(msg), "Receive returned with EAGAIN or EWOULDBLOCK")
        self.client_socket.stop()
        self.client_socket.close()
        
if __name__ == '__main__':
    unittest.main()
