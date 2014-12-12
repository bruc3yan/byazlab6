# import socket
# port = 5006
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind(("", port))
# print "waiting on port:", port
# while 1:
#     data, addr = server_socket.recvfrom(1024)
#     print data
import threading
import time
import SocketServer
#usage: python server.py

class ClientRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Client listener")
        cur_thread_name = threading.current_thread().getName()
        print("{} hears (out of {}) from {} : ".format(cur_thread_name, threading.active_count(), self.client_address))
        print(data)
        socket.sendto(data.upper(), self.client_address)


class ServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Server listener")
        cur_thread = threading.current_thread().getName()
        print("{} hears (out of {}) from server {} : ".format(cur_thread, threading.active_count(), self.client_address))
        print(data)
        socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): 
        pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 8000
    thread_name = threading.current_thread().name

    if "MainThread" in thread_name:
    	# port 8001 -> client messages comes here
	    client_interface = ThreadedUDPServer((HOST,PORT+1), ClientRequestHandler)
	    client_listener = threading.Thread(target=client_interface.serve_forever)
	    client_listener.setDaemon(True)
	    client_listener.setName('GotDamnUDP')
	    print client_listener.getName()
	    print threading.active_count()
	    print("Client listener at port", PORT+1)
	    client_listener.start()
	    print threading.active_count()

	    # port 8000 -> server messages comes here
	    server_interface = ThreadedUDPServer((HOST,PORT), ServerRequestHandler) 
	    server_listener = threading.Thread(target=server_interface.serve_forever)
	    server_listener.setDaemon(True)
	    print("Server listener at port", PORT)
	    server_listener.start()
	    print threading.active_count()

    while 1:
    	time.sleep(1)